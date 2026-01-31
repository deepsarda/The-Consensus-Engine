import sys
import json
import argparse
from termcolor import colored
from forensics import ForensicAnalyzer
from council import Council
from judge import JudgeAgent


def main():
    parser = argparse.ArgumentParser(
        description="The Consensus Engine: Multi-LLM Misinformation Detection"
    )
    parser.add_argument("--claim", type=str, help="The text claim to verify")
    parser.add_argument("--image", type=str, help="Path to the image file")
    parser.add_argument("--demo", action="store_true", help="Run the shark demo case")

    args = parser.parse_args()

    if args.demo:
        print(colored("Running Demo Case: Shark in Subway", "cyan"))
        claim = (
            "Breaking: A shark swimming in a flooded subway station during the storm!"
        )
        media_path = "/path/to/shark_subway.jpg"
        media_type = "Image"
    elif args.claim and args.image:
        claim = args.claim
        media_path = args.image
        media_type = "Image"
    else:
        print("Please provide --claim and --image, or use --demo")
        return

    print(colored(f"\n[1] Analyzing Claim: '{claim}'", "white", attrs=["bold"]))
    print(colored("Gathering Forensic Evidence...", "yellow"))

    analyzer = ForensicAnalyzer()
    forensics = analyzer.run_all(media_path, claim)
    print(json.dumps(forensics, indent=2))

    print(colored("\n[2] Convening the Council of LLMs...", "yellow"))

    council = Council()
    council_results = council.convene(claim, media_type, forensics)

    for res in council_results:
        if "error" in res:
            print(colored(f"Member Failed: {res.get('error')}", "red"))
        else:
            name = res.get("member_name")
            verdict = res.get("output", {}).get("verdict", "Unknown")
            conf = res.get("output", {}).get("confidence_score", 0)
            print(colored(f"\n--- {name} ---", "blue", attrs=["bold"]))
            print(f"Verdict: {verdict} (Confidence: {conf}%)")

    print(colored("\n[3] The Adjudicator is deliberating...", "yellow"))

    judge = JudgeAgent()
    final_verdict = judge.adjudicate(forensics, council_results)

    print(colored("\n---- FINAL JUDGEMENT ---", "green", attrs=["bold"]))
    print(json.dumps(final_verdict, indent=2))


if __name__ == "__main__":
    main()
