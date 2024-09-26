import click
import os
from core import gen_and_save_seq


@click.group()
def cli():
    """Generate and plot sequences."""
    pass


@cli.command()
@click.option('--n_terms', default=300, help='Number of terms in each sequence')
@click.option('--num_prev_terms', default=2, help='Number of previous terms to consider')
@click.option('--num_values_tot', default=6, help='Total number of possible values')
@click.option('--num_random_seeds', default=100, help='Number of random seeds to use')
def generate(n_terms, num_prev_terms, num_values_tot, num_random_seeds):
    """Generate multiple sequences."""
    foldername = f"sequences/p{num_prev_terms}_v{num_values_tot}_t{n_terms}"

    for random_seed in range(num_random_seeds):
        _, _, _ = gen_and_save_seq(n_terms, random_seed, num_prev_terms, num_values_tot, foldername, show_plot=False)

    click.echo(f"Generated {num_random_seeds} sequences in {foldername}")


@cli.command()
@click.option('--n_terms', default=1000, help='Number of terms in the sequence')
@click.option('--random_seed', default=468, help='Random seed for the sequence')
@click.option('--num_prev_terms', default=2, help='Number of previous terms to consider')
@click.option('--num_values_tot', default=6, help='Total number of possible values')
def plot(n_terms, random_seed, num_prev_terms, num_values_tot):
    """Plot an individual sequence."""

    foldername = "sequences/single_plots"

    seq, formula_latex, formula_ops = gen_and_save_seq(
        n_terms, random_seed, num_prev_terms, num_values_tot, foldername, show_plot=True
    )

    click.echo(f"Plotted sequence with seed {random_seed} in {foldername}")


if __name__ == '__main__':
    cli()
