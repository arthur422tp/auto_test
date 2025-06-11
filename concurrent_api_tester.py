#!/usr/bin/env python3
"""Concurrent API stress tester using asyncio and aiohttp."""

import asyncio
import time
from typing import Dict, Any, List, Optional

import aiohttp


class ConcurrentApiTester:
    """Send many concurrent requests to a single endpoint."""

    def __init__(
        self,
        base_url: str,
        endpoint: str,
        method: str = "GET",
        num_requests: int = 100,
        concurrency: int = 10,
        timeout: int = 10,
        headers: Optional[Dict[str, str]] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.endpoint = endpoint
        self.url = f"{self.base_url}{self.endpoint}"
        self.method = method.upper()
        self.num_requests = num_requests
        self.concurrency = concurrency
        self.timeout = timeout
        self.headers = headers or {"Content-Type": "application/json"}
        self.data = data
        self.results: List[Dict[str, Any]] = []

    async def _run_single(self, session: aiohttp.ClientSession, sem: asyncio.Semaphore) -> None:
        """Execute a single request and record statistics."""
        async with sem:
            start = time.time()
            result: Dict[str, Any] = {
                "method": self.method,
                "url": self.url,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "success": False,
                "status_code": None,
                "response_time": 0.0,
                "error": None,
                "response_data": None,
            }
            try:
                async with session.request(
                    self.method,
                    self.url,
                    json=self.data if self.data else None,
                    timeout=self.timeout,
                ) as resp:
                    elapsed = time.time() - start
                    result["response_time"] = round(elapsed, 3)
                    result["status_code"] = resp.status
                    try:
                        result["response_data"] = await resp.json()
                    except Exception:
                        text = await resp.text()
                        result["response_data"] = text[:200]
                    result["success"] = 200 <= resp.status < 300
            except Exception as e:  # network or timeout error
                result["error"] = str(e)
            self.results.append(result)

    async def run_tests(self) -> None:
        """Run the stress test."""
        sem = asyncio.Semaphore(self.concurrency)
        timeout = aiohttp.ClientTimeout(total=None)
        async with aiohttp.ClientSession(headers=self.headers, timeout=timeout) as session:
            tasks = [self._run_single(session, sem) for _ in range(self.num_requests)]
            await asyncio.gather(*tasks)

    def print_summary(self) -> None:
        """Print summary statistics for the run."""
        total = len(self.results)
        successes = sum(1 for r in self.results if r["success"])
        times = [r["response_time"] for r in self.results if r["response_time"] > 0]
        success_rate = (successes / total * 100) if total else 0
        avg_time = sum(times) / len(times) if times else 0
        max_time = max(times) if times else 0
        min_time = min(times) if times else 0

        print("=" * 60)
        print("📊 壓力測試結果")
        print("=" * 60)
        print(f"URL: {self.url}")
        print(f"方法: {self.method}")
        print(f"總請求數: {total}")
        print(f"成功請求: {successes}")
        print(f"成功率: {success_rate:.1f}%")
        print(f"平均回應時間: {avg_time:.3f}s")
        print(f"最快回應時間: {min_time:.3f}s")
        print(f"最慢回應時間: {max_time:.3f}s")

    def generate_report(self, output_file: str) -> None:
        """Generate JSON report."""
        import json

        report = {
            "summary": {
                "total_requests": len(self.results),
                "successful_requests": sum(1 for r in self.results if r["success"]),
                "success_rate": (
                    sum(1 for r in self.results if r["success"]) / len(self.results) * 100
                    if self.results
                    else 0
                ),
                "average_time": (
                    sum(r["response_time"] for r in self.results) / len(self.results)
                    if self.results
                    else 0
                ),
                "max_time": max((r["response_time"] for r in self.results), default=0),
                "min_time": min((r["response_time"] for r in self.results), default=0),
            },
            "results": self.results,
        }

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"📄 JSON 報告已生成: {output_file}")

    def generate_html_report(self, json_file: str, html_file: str) -> None:
        """Generate HTML report from JSON using ReportGenerator."""
        from report_generator import ReportGenerator
        import json

        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        generator = ReportGenerator(data.get("results", []))
        # modify summary card to include extra metrics if necessary
        generator.generate_html_report(html_file)

