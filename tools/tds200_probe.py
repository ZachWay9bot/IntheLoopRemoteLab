"""Local TDS210/220 probe; does not require a GitHub token."""
import argparse
import json
from remotelab.adapters.tds200 import TektronixTDS200Adapter


def main():
    parser = argparse.ArgumentParser(description="Tektronix TDS200 serial probe")
    parser.add_argument("--port", default="COM11")
    parser.add_argument("--baudrate", type=int, default=9600)
    parser.add_argument("--flow-control", choices=["none", "rtscts", "xonxoff"],
                        default="none")
    parser.add_argument("--action",
                        choices=["identify", "diagnose", "measure", "capture_waveform"],
                        default="identify")
    parser.add_argument("--channel", choices=["CH1", "CH2"], default="CH1")
    parser.add_argument("--kind",
                        choices=["frequency", "period", "vpp", "mean", "rms"],
                        default="frequency")
    parser.add_argument("--max-points", type=int, default=250)
    args = parser.parse_args()
    adapter = TektronixTDS200Adapter(port=args.port, baudrate=args.baudrate,
                                      flow_control=args.flow_control)
    kwargs = ({"channel": args.channel, "max_points": args.max_points}
              if args.action == "capture_waveform" else
              {"channel": args.channel, "kind": args.kind}
              if args.action == "measure" else {})
    print(json.dumps(getattr(adapter, args.action)(**kwargs), indent=2))


if __name__ == "__main__":
    main()
