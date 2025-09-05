import argparse
import matplotlib.pyplot as plt
import json
from . import plotter

def main():
    parser = argparse.ArgumentParser(description="Band Diagram Plotter (CUI)", conflict_handler='resolve')
    
    # Add config file argument first
    parser.add_argument('--json', dest='config', type=str, help='Path to the configuration file (JSON format)')

    # Add other arguments, they will override config file settings
    parser.add_argument('--view', dest='view', choices=['before', 'after'], default='after', help='Select the view: before or after junction')
    parser.add_argument('--chi', dest='chi', type=float, help='Electron affinity (eV)')
    parser.add_argument('--eg', dest='eg', type=float, help='Band gap (eV)')
    parser.add_argument('--fermi-shift', dest='fermi_shift', type=float, help='Fermi level shift from intrinsic (eV). Positive for n-type, negative for p-type.')
    parser.add_argument('--wf-left', dest='wf_left', type=float, help='Work function of the left electrode (eV)')
    parser.add_argument('--label-left', dest='label_left', type=str, help='Label for the left electrode')
    parser.add_argument('--wf-right', dest='wf_right', type=float, help='Work function of the right electrode (eV)')
    parser.add_argument('--label-right', dest='label_right', type=str, help='Label for the right electrode')
    parser.add_argument('--bias', dest='bias', type=float, help='Bias voltage (V)')
    parser.add_argument('--output', dest='output', type=str, help='Output filename (e.g., band_diagram.png)')

    args = parser.parse_args()

    # Default parameters
    config = {
        'view': 'after',
        'chi': 4.05,
        'eg': 1.12,
        'fermi_shift': 0.2,
        'wf_left': 4.2,
        'label_left': 'Al',
        'wf_right': 5.1,
        'label_right': 'Au',
        'bias': 0.0,
        'output': None
    }

    # Load from config file if specified
    if args.config:
        try:
            with open(args.config, 'r') as f:
                config.update(json.load(f))
        except FileNotFoundError:
            print(f"Error: JSON file not found at {args.config}")
            return
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from {args.config}")
            return

    # Create a dictionary from the parsed args, excluding None values
    # argparse converts hyphens to underscores automatically.
    cli_args = {k: v for k, v in vars(args).items() if v is not None and k != 'config'}
    
    # Update config with CLI arguments, giving CLI precedence
    config.update(cli_args)

    fig, ax = plt.subplots(figsize=(10, 7))
    
    # Separate view and output file from drawing parameters
    view_type = config.pop('view', 'after')
    output_file = config.pop('output', None)
    
    if view_type == 'before':
        plotter.draw_pre_junction_diagram(ax, **config)
    else:
        plotter.draw_band_diagram(ax, **config)
    
    if output_file:
        fig.tight_layout(rect=[0, 0, 0.85, 1])
        plt.savefig(output_file, bbox_inches='tight')
        print(f"Band diagram saved to {output_file}")
    else:
        fig.tight_layout(rect=[0, 0, 0.85, 1])
        plt.show()

if __name__ == "__main__":
    main()
