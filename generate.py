#!/usr/bin/env python3
"""
AI Robots.txt Generator
Generate an optimized robots.txt for AI search engine crawlers.

Usage:
    python generate.py --domain example.com
    python generate.py --domain example.com --output robots.txt
    python generate.py --domain example.com --block GPTBot,Bytespider

More info: https://geoscoreai.com/blog/robots-txt-ai-crawlers
"""

import argparse
import sys
from datetime import datetime

AI_CRAWLERS = {
    "GPTBot": {"operator": "OpenAI", "product": "ChatGPT", "docs": "https://platform.openai.com/docs/gptbot"},
    "ChatGPT-User": {"operator": "OpenAI", "product": "ChatGPT Browse", "docs": "https://platform.openai.com/docs/plugins/bot"},
    "OAI-SearchBot": {"operator": "OpenAI", "product": "ChatGPT Search", "docs": "https://platform.openai.com/docs/bots"},
    "PerplexityBot": {"operator": "Perplexity", "product": "Perplexity AI", "docs": "https://docs.perplexity.ai/docs/perplexity-bot"},
    "Google-Extended": {"operator": "Google", "product": "Gemini / AI Overviews", "docs": "https://developers.google.com/search/docs/crawling-indexing/google-common-crawlers"},
    "ClaudeBot": {"operator": "Anthropic", "product": "Claude", "docs": "https://www.anthropic.com/crawlers"},
    "Applebot-Extended": {"operator": "Apple", "product": "Apple Intelligence", "docs": "https://support.apple.com/en-us/111325"},
    "Meta-ExternalAgent": {"operator": "Meta", "product": "Meta AI", "docs": "https://developers.facebook.com/docs/sharing/webmasters/crawler"},
    "cohere-ai": {"operator": "Cohere", "product": "Cohere AI", "docs": ""},
    "Bytespider": {"operator": "ByteDance", "product": "Doubao / TikTok", "docs": ""},
}

STANDARD_CRAWLERS = ["Googlebot", "Bingbot", "Yandex", "DuckDuckBot"]


def generate_robots_txt(
    domain: str,
    block: list[str] | None = None,
    allow_only: list[str] | None = None,
    disallow_paths: list[str] | None = None,
    crawl_delay: int | None = None,
    sitemaps: list[str] | None = None,
) -> str:
    block = block or []
    disallow_paths = disallow_paths or []

    lines = []
    lines.append("# ============================================")
    lines.append(f"# Robots.txt for {domain}")
    lines.append(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("# Generator: https://github.com/henu-wang/ai-robots-txt-generator")
    lines.append("# Guide: https://geoscoreai.com/blog/robots-txt-ai-crawlers")
    lines.append("# ============================================")
    lines.append("")

    # AI Crawlers section
    lines.append("# ============================================")
    lines.append("# AI Search Engine Crawlers")
    lines.append("# ============================================")
    lines.append("")

    for crawler, info in AI_CRAWLERS.items():
        if allow_only and crawler not in allow_only:
            continue

        comment = f"# {info['operator']} - {info['product']}"
        if info["docs"]:
            comment += f" ({info['docs']})"
        lines.append(comment)
        lines.append(f"User-agent: {crawler}")

        if crawler in block:
            lines.append("Disallow: /")
        else:
            lines.append("Allow: /")
            for path in disallow_paths:
                lines.append(f"Disallow: {path}")
            if crawl_delay:
                lines.append(f"Crawl-delay: {crawl_delay}")

        lines.append("")

    # Standard crawlers
    lines.append("# ============================================")
    lines.append("# Standard Search Engine Crawlers")
    lines.append("# ============================================")
    lines.append("")

    for crawler in STANDARD_CRAWLERS:
        lines.append(f"User-agent: {crawler}")
        lines.append("Allow: /")
        for path in disallow_paths:
            lines.append(f"Disallow: {path}")
        lines.append("")

    # Default rule
    lines.append("# Default rule for all other crawlers")
    lines.append("User-agent: *")
    lines.append("Allow: /")
    for path in disallow_paths:
        lines.append(f"Disallow: {path}")
    lines.append("")

    # Sitemaps
    lines.append("# ============================================")
    lines.append("# Sitemaps")
    lines.append("# ============================================")

    if sitemaps:
        for sitemap in sitemaps:
            lines.append(f"Sitemap: {sitemap}")
    else:
        lines.append(f"Sitemap: https://{domain}/sitemap.xml")

    lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Generate an optimized robots.txt for AI search engine crawlers",
        epilog="More info: https://geoscoreai.com/blog/robots-txt-ai-crawlers",
    )
    parser.add_argument("--domain", required=True, help="Your domain (e.g., example.com)")
    parser.add_argument("--output", "-o", help="Output file path (default: stdout)")
    parser.add_argument("--block", help="Comma-separated list of AI crawlers to block")
    parser.add_argument("--allow-only", help="Comma-separated list of AI crawlers to allow (blocks all others)")
    parser.add_argument("--disallow", help="Comma-separated list of paths to disallow")
    parser.add_argument("--crawl-delay", type=int, help="Crawl delay in seconds")
    parser.add_argument("--sitemap", help="Comma-separated list of sitemap URLs")
    parser.add_argument("--list-crawlers", action="store_true", help="List all known AI crawlers")

    args = parser.parse_args()

    if args.list_crawlers:
        print(f"{'Crawler':<25} {'Operator':<15} {'Product':<25}")
        print("-" * 65)
        for crawler, info in AI_CRAWLERS.items():
            print(f"{crawler:<25} {info['operator']:<15} {info['product']:<25}")
        return

    block = args.block.split(",") if args.block else None
    allow_only = args.allow_only.split(",") if args.allow_only else None
    disallow_paths = args.disallow.split(",") if args.disallow else None
    sitemaps = args.sitemap.split(",") if args.sitemap else None

    result = generate_robots_txt(
        domain=args.domain,
        block=block,
        allow_only=allow_only,
        disallow_paths=disallow_paths,
        crawl_delay=args.crawl_delay,
        sitemaps=sitemaps,
    )

    if args.output:
        with open(args.output, "w") as f:
            f.write(result)
        print(f"robots.txt written to {args.output}")
        print(f"\nVerify your configuration: https://geoscoreai.com/checks/robots-txt")
    else:
        print(result)


if __name__ == "__main__":
    main()
