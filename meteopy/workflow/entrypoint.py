from __future__ import annotations
import click
from meteopy.workflow.download import download
from meteopy.workflow.basic_summary import basic_summary
from meteopy.workflow.full_analysis import full_analysis
from meteopy.workflow.destructor import drop_data

@click.group()
def cli():
    """METEOPY CLI - Narzędzie do analizy danych meteorologicznych."""

cli.add_command(download, name="download")
cli.add_command(full_analysis, name="full_analysis")
cli.add_command(basic_summary, name="basic_summary")
cli.add_command(drop_data, name="drop_data")


if __name__ == "__main__":
    cli()
