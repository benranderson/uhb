"""Tests for cli module."""

import pytest
import json

import click

from click.testing import CliRunner

import cli

test_inputs = {"D_o": 0.1731, "f": 0.6}


# def test_command_line_interface():
#     """Test the CLI."""
#     runner = CliRunner()
#     with runner.isolated_filesystem():
#         with open("inputs.json", "w") as f:
#             json.dump(test_inputs, f)

#         result = runner.invoke(cli.main, ["inputs.json"])
#         assert result.exit_code == 0
#         assert "Calculating soil stiffnesses..." in result.output

#         help_result = runner.invoke(cli.main, ["--help"])
#         assert help_result.exit_code == 0
#         assert "--help  Show this message and exit." in help_result.output
