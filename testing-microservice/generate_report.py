import argparse
import xml.etree.ElementTree as ET
from datetime import datetime


def generate_report(xml_path: str, service: str, env: str, out_path: str):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    testsuite = root if root.tag == "testsuite" else root.find("testsuite")

    total = int(testsuite.attrib.get("tests", 0))
    failures = int(testsuite.attrib.get("failures", 0))
    errors = int(testsuite.attrib.get("errors", 0))
    skipped = int(testsuite.attrib.get("skipped", 0))
    passed = total - failures - errors - skipped
    duration = float(testsuite.attrib.get("time", 0))

    lines = [
        "=" * 60,
        "TEST REPORT",
        "=" * 60,
        f"Service:     {service}",
        f"Environment: {env}",
        f"Generated:   {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC",
        "-" * 60,
        f"Total:       {total}",
        f"Passed:      {passed}",
        f"Failed:      {failures}",
        f"Errors:      {errors}",
        f"Skipped:     {skipped}",
        f"Duration:    {duration:.2f}s",
        "-" * 60,
        "TEST CASES",
        "-" * 60,
    ]

    for testcase in testsuite.findall("testcase"):
        name = testcase.attrib.get("name")
        classname = testcase.attrib.get("classname")
        time = testcase.attrib.get("time", "0")

        failure = testcase.find("failure")
        error = testcase.find("error")
        skipped_el = testcase.find("skipped")

        if failure is not None:
            status = "FAILED"
            message = failure.attrib.get("message", "")
        elif error is not None:
            status = "ERROR"
            message = error.attrib.get("message", "")
        elif skipped_el is not None:
            status = "SKIPPED"
            message = skipped_el.attrib.get("message", "")
        else:
            status = "PASSED"
            message = ""

        lines.append(f"[{status}] {classname}::{name} ({time}s)")
        if message:
            lines.append(f"         {message}")

    lines.append("=" * 60)
    overall = "PASSED" if failures == 0 and errors == 0 else "FAILED"
    lines.append(f"OVERALL RESULT: {overall}")
    lines.append("=" * 60)

    with open(out_path, "w") as f:
        f.write("\n".join(lines))

    print("\n".join(lines))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--xml", required=True)
    parser.add_argument("--service", required=True)
    parser.add_argument("--env", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    generate_report(args.xml, args.service, args.env, args.out)
