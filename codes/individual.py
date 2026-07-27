import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import os

# 1. Find all Bracken files
bracken_files = sorted(
    glob.glob("*.bracken*")
)

if len(bracken_files) == 0:
    raise FileNotFoundError(
        "No Bracken files found"
    )

print(
    "Number of Bracken files:",
    len(bracken_files)
)

# 2. Store species tables
species_tables = []

for file in bracken_files:

    # Extract sample name
    sample = os.path.basename(file).replace(
        ".bracken.species",
        ""
    )

    print(
        "Processing:",
        sample
    )

    # Read Bracken file
    df = pd.read_csv(
        file,
        sep="\t"
    )

    # Keep species level only
    df = df[
        df["taxonomy_lvl"] == "S"
    ]

    # Keep required columns
    df = df[
        [
            "name",
            "fraction_total_reads"
        ]
    ]

    # Rename columns
    df.columns = [
        "Species",
        sample
    ]

    species_tables.append(
        df
    )

# 3. Merge all samples together
merged = species_tables[0]

for df in species_tables[1:]:

    merged = merged.merge(
        df,
        on="Species",
        how="outer"
    )

# Replace missing values with zero
merged = merged.fillna(0)

# Set Species as index
merged = merged.set_index(
    "Species"
)

# 4. Create a table containing the top 15 species
#    for each individual sample

top_species_per_sample = {}

for sample in merged.columns:

    top15 = (
        merged[sample]
        .sort_values(
            ascending=False
        )
        .head(15)
    )

    top_species_per_sample[sample] = top15.index

# 5. Create a common list of species
#    appearing in the top 15 of at least one sample

all_top_species = set()

for species_list in (
    top_species_per_sample.values()
):

    all_top_species.update(
        species_list
    )

# Convert to list
all_top_species = list(
    all_top_species
)

# 6. Create the final plotting table
plot_table = pd.DataFrame(
    index=all_top_species,
    columns=merged.columns
)

# Fill the table with abundance values
for sample in merged.columns:

    # Keep only species that are among
    # the top species for that sample

    top_species = (
        top_species_per_sample[sample]
    )

    for species in top_species:

        plot_table.loc[
            species,
            sample
        ] = merged.loc[
            species,
            sample
        ]

# Replace missing values with zero
plot_table = plot_table.fillna(0)

# 7. Add all remaining species as "Others"
others = (
    merged.sum(axis=0)
    - plot_table.sum(axis=0)
)

plot_table.loc[
    "Others"
] = others

# 8. Convert to percentages for each sample
plot_table = (
    plot_table
    .div(
        plot_table.sum(axis=0),
        axis=1
    )
) * 100

# 9. Plot all samples in one figure
sns.set_style(
    "white"
)

fig, ax = plt.subplots(
    figsize=(18, 10)
)

# Create a colour palette
colors = sns.color_palette(
    "tab20",
    n_colors=len(plot_table.index)
)

# Make Others grey
species_colors = {}

for species, color in zip(
    plot_table.index,
    colors
):

    species_colors[
        species
    ] = color

species_colors[
    "Others"
] = "lightgrey"

# Start position of each stack
bottom = pd.Series(
    0,
    index=plot_table.columns
)

# Plot each species
for species in plot_table.index:

    ax.bar(
        plot_table.columns,
        plot_table.loc[
            species
        ],
        bottom=bottom,
        label=species,
        color=species_colors[
            species
        ],
        edgecolor="white",
        linewidth=0.3
    )

    # Update bottom position
    bottom += plot_table.loc[
        species
    ]

# 10. Formatting
ax.set_ylabel(
    "Relative abundance (%)",
    fontsize=14
)

ax.set_xlabel(
    "Samples",
    fontsize=14
)

ax.set_title(
    "Top 15 Species Abundance per Sample",
    fontsize=18
)

ax.set_ylim(
    0,
    100
)

# Rotate sample names
plt.xticks(
    rotation=90
)

# Add legend outside plot
ax.legend(
    title="Species",
    bbox_to_anchor=(
        1.02,
        1
    ),
    loc="upper left",
    fontsize=9
)

plt.tight_layout()

# Save the combined figure
plt.savefig(
    "Top15_Species_All_Samples.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("Plot saved")
