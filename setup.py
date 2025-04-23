from setuptools import setup, find_packages

setup(
    name="scp_tag_parser",
    version="0.1.0",
    description="SCP財団タグリスト解析システム",
    long_description="""
    SCP財団日本語Wikiのタグリスト（Wikidotソース）を解析し、
    各タグに関する情報を網羅的に抽出し、構造化されたJSONファイルとして出力するシステム。
    """,
    author="SCP-JP",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pydantic>=2.0.0",
    ],
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "scp-tag-parser=scp_tag_parser.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)