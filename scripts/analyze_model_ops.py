import argparse
import importlib.util
import json
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Tuple

import torch
import torch.nn as nn

try:
    import yaml
except ImportError:
    yaml = None

ANALYZER_VERSION = "0.1.0"

DEFAULT_MAPPING = {
    "linear_mac": "MAC",
    "conv_mac": "MAC",
    "bias_add": "ADD",
    "residual_add": "ADD",
    "relu": "NON_LINEAR",
    "tanh": "NON_LINEAR",
    "sigmoid": "NON_LINEAR",
    "gelu": "NON_LINEAR",
    "batchnorm": "NORMALIZATION",
    "layernorm": "NORMALIZATION",
    "maxpool": "POOLING",
    "avgpool": "POOLING",
    "flatten": "DATA_MOVEMENT",
    "reshape": "DATA_MOVEMENT",
    "transpose": "DATA_MOVEMENT",
    "unsupported": "UNSUPPORTED",
}


def parse_shape(shape_text: str) -> Tuple[int, ...]:
    values = [v.strip() for v in shape_text.split(",") if v.strip()]
    if not values:
        raise ValueError("input-shape must contain at least one dimension")
    return tuple(int(v) for v in values)


def load_module_from_file(file_path: Path):
    spec = importlib.util.spec_from_file_location("user_model_module", file_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to import module from {file_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def instantiate_model(module: Any, class_name: str, kwargs_json: str) -> nn.Module:
    if not hasattr(module, class_name):
        raise AttributeError(f"Model class '{class_name}' not found in module")
    cls = getattr(module, class_name)

    kwargs: Dict[str, Any] = {}
    if kwargs_json:
        kwargs = json.loads(kwargs_json)
        if not isinstance(kwargs, dict):
            raise ValueError("model-kwargs must be a JSON object")

    model = cls(**kwargs)
    if not isinstance(model, nn.Module):
        raise TypeError("Instantiated object is not a torch.nn.Module")
    model.eval()
    return model


def maybe_load_mapping(mapping_file: Path) -> Dict[str, str]:
    if not mapping_file.exists() or yaml is None:
        return DEFAULT_MAPPING
    with mapping_file.open("r", encoding="utf-8") as f:
        loaded = yaml.safe_load(f) or {}
    mapping = loaded.get("operation_to_hardware_unit", {})
    if not isinstance(mapping, dict):
        return DEFAULT_MAPPING
    merged = dict(DEFAULT_MAPPING)
    merged.update({str(k): str(v) for k, v in mapping.items()})
    return merged


def numel(shape: Tuple[int, ...]) -> int:
    n = 1
    for d in shape:
        n *= int(d)
    return int(n)


def count_layer_ops(module: nn.Module, in_shape: Tuple[int, ...], out_shape: Tuple[int, ...]) -> List[Dict[str, Any]]:
    records: List[Dict[str, Any]] = []

    if isinstance(module, nn.Linear):
        batch = int(in_shape[0]) if len(in_shape) > 0 else 1
        mac_count = batch * int(module.in_features) * int(module.out_features)
        records.append({"operation_type": "linear_mac", "count": mac_count, "notes": "Linear MAC operations"})
        if module.bias is not None:
            records.append({"operation_type": "bias_add", "count": batch * int(module.out_features), "notes": "Linear bias additions"})
        return records

    if isinstance(module, nn.Conv2d):
        batch = int(out_shape[0])
        out_channels = int(out_shape[1])
        out_h = int(out_shape[2])
        out_w = int(out_shape[3])
        k_h, k_w = module.kernel_size
        in_channels = int(module.in_channels)
        groups = int(module.groups)
        mac_per_output = (in_channels // groups) * int(k_h) * int(k_w)
        mac_count = batch * out_channels * out_h * out_w * mac_per_output
        records.append({"operation_type": "conv_mac", "count": mac_count, "notes": "Conv2d MAC operations"})
        if module.bias is not None:
            records.append({"operation_type": "bias_add", "count": batch * out_channels * out_h * out_w, "notes": "Conv2d bias additions"})
        return records

    if isinstance(module, nn.ReLU):
        records.append({"operation_type": "relu", "count": numel(out_shape), "notes": "ReLU elementwise non-linearity"})
        return records

    if isinstance(module, nn.Tanh):
        records.append({"operation_type": "tanh", "count": numel(out_shape), "notes": "Tanh elementwise non-linearity"})
        return records

    if isinstance(module, nn.Sigmoid):
        records.append({"operation_type": "sigmoid", "count": numel(out_shape), "notes": "Sigmoid elementwise non-linearity"})
        return records

    if isinstance(module, nn.GELU):
        records.append({"operation_type": "gelu", "count": numel(out_shape), "notes": "GELU elementwise non-linearity"})
        return records

    if isinstance(module, (nn.BatchNorm1d, nn.BatchNorm2d)):
        records.append({"operation_type": "batchnorm", "count": numel(out_shape), "notes": "BatchNorm normalization operations (approximate)"})
        return records

    if isinstance(module, nn.LayerNorm):
        records.append({"operation_type": "layernorm", "count": numel(out_shape), "notes": "LayerNorm normalization operations (approximate)"})
        return records

    if isinstance(module, (nn.MaxPool1d, nn.MaxPool2d)):
        records.append({"operation_type": "maxpool", "count": numel(out_shape), "notes": "MaxPool operations (output-element approximation)"})
        return records

    if isinstance(module, (nn.AvgPool1d, nn.AvgPool2d)):
        records.append({"operation_type": "avgpool", "count": numel(out_shape), "notes": "AvgPool operations (output-element approximation)"})
        return records

    if isinstance(module, nn.Flatten):
        records.append({"operation_type": "flatten", "count": numel(out_shape), "notes": "Flatten data movement"})
        return records

    if isinstance(module, nn.Identity):
        return records

    records.append({"operation_type": "unsupported", "count": 0, "notes": f"Unsupported module type: {module.__class__.__name__}"})
    return records


def attach_shape_hooks(model: nn.Module):
    shape_cache: Dict[str, Dict[str, Tuple[int, ...]]] = {}
    hooks = []

    for name, module in model.named_modules():
        if name == "":
            continue

        def make_hook(layer_name: str):
            def hook(_module, inp, out):
                in_shape = tuple(inp[0].shape) if inp and hasattr(inp[0], "shape") else tuple()
                out_shape = tuple(out.shape) if hasattr(out, "shape") else tuple()
                shape_cache[layer_name] = {"in": in_shape, "out": out_shape}

            return hook

        hooks.append(module.register_forward_hook(make_hook(name)))

    return shape_cache, hooks


def analyze_model(model: nn.Module, input_shape: Tuple[int, ...], mapping: Dict[str, str]) -> Dict[str, Any]:
    shape_cache, hooks = attach_shape_hooks(model)

    with torch.no_grad():
        dummy = torch.randn(*input_shape)
        _ = model(dummy)

    for h in hooks:
        h.remove()

    layers: List[Dict[str, Any]] = []
    op_totals = Counter()
    hw_totals = Counter()
    unsupported_layers: List[str] = []

    for name, module in model.named_modules():
        if name == "":
            continue
        if name not in shape_cache:
            continue

        in_shape = shape_cache[name]["in"]
        out_shape = shape_cache[name]["out"]
        op_records = count_layer_ops(module, in_shape, out_shape)

        for op in op_records:
            operation_type = str(op["operation_type"])
            mapped_hw = mapping.get(operation_type, mapping["unsupported"])
            count = int(op["count"])
            note = str(op["notes"])

            row = {
                "layer_name": name,
                "module_type": module.__class__.__name__,
                "operation_type": operation_type,
                "mapped_hardware_unit": mapped_hw,
                "operation_count": count,
                "notes": note,
            }
            layers.append(row)
            op_totals[operation_type] += count
            hw_totals[mapped_hw] += count
            if operation_type == "unsupported":
                unsupported_layers.append(name)

    return {
        "layers": layers,
        "totals": {
            "operation_type_totals": dict(op_totals),
            "hardware_unit_totals": dict(hw_totals),
            "unsupported_layers": sorted(set(unsupported_layers)),
        },
    }


def main():
    parser = argparse.ArgumentParser(description="Analyze Python model operations and map to hardware-unit demand")
    parser.add_argument("--model-file", required=True, help="Path to Python file containing the model class")
    parser.add_argument("--model-class", required=True, help="Class name of torch.nn.Module in model-file")
    parser.add_argument("--input-shape", required=True, help="Comma-separated input shape, example: 1,128")
    parser.add_argument("--model-kwargs", default="", help="Optional JSON object for model constructor kwargs")
    parser.add_argument("--mapping-file", default="configs/hardware_unit_taxonomy.yaml", help="Path to operation mapping config")
    parser.add_argument("--output", required=True, help="Output JSON file path")

    args = parser.parse_args()

    model_file = Path(args.model_file)
    if not model_file.exists():
        raise FileNotFoundError(f"Model file not found: {model_file}")

    input_shape = parse_shape(args.input_shape)
    mapping = maybe_load_mapping(Path(args.mapping_file))

    module = load_module_from_file(model_file)
    model = instantiate_model(module, args.model_class, args.model_kwargs)
    analysis = analyze_model(model, input_shape, mapping)

    output = {
        "metadata": {
            "model_file": str(model_file),
            "model_class": args.model_class,
            "input_shape": list(input_shape),
            "analyzer_version": ANALYZER_VERSION,
        },
        "layers": analysis["layers"],
        "totals": analysis["totals"],
    }

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print(f"Wrote analysis to {output_path}")


if __name__ == "__main__":
    main()
