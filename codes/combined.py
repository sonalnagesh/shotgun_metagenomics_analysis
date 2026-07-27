import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import os

# Find all Bracken files
bracken_files = sorted(glob.glob("*.bracken*"))

if len(bracken_files) == 0:
    raise FileNotFoundError("No Bracken files found")

print("Bracken files:", len(bracken_files))

# Store species-level tables
species_tables = []

for file in bracken_files:

    sample = os.path.basename(file).replace(
        ".bracken.species",
        ""
    )

    print("Processing:", sample)

    df = pd.read_csv(
        file,
        sep="\t"
    )

    # Keep species level only
    df = df[df["taxonomy_lvl"] == "S"]

    # Keep required columns
    df = df[[
        "name",
        "fraction_total_reads"
    ]]

    # Rename columns
    df.columns = [
        "Species",
        sample
    ]

    species_tables.append(df)

# Merge all samples by species
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
merged = merged.set_index("Species")

print("Merged table:", merged.shape)

# Calculate combined abundance across all samples
combined_abundance = merged.sum(axis=1)

# Select top 15 species
top15 = (
    combined_abundance
    .sort_values(ascending=False)
    .head(15)
)

# Combine all remaining species into "Others"
others = (
    combined_abundance
    .drop(top15.index)
    .sum()
)

# Create final plotting data
plot_data = pd.concat([
    top15,
    pd.Series({
        "Others": others
    })
])

# Convert to percentages
plot_data = (
    plot_data / plot_data.sum()
) * 100

# Create plot
fig, ax = plt.subplots(
    figsize=(4, 8)
)

sns.set_style("white")

# Create colour palette
colors = sns.color_palette(
    "tab20",
    n_colors=len(top15)
)

# Add colour for Others
colors = list(colors) + ["grey"]

bottom = 0

# Create stacked bar
for species, color in zip(
    plot_data.index,
    colors
):

    value = plot_data[species]

    ax.bar(
        "Combined",
        value,
        bottom=bottom,
        color=color,
        width=0.6,
        label=species
    )

    bottom += value

# Axis labels
ax.set_ylabel(
    "Relative abundance (%)",
    fontsize=12
)

ax.set_ylim(
    0,
    100
)

ax.set_title(
    "Species (ALL Samples)",
    fontsize=14
)

# Add legend
ax.legend(
    bbox_to_anchor=(1.05, 1),
    loc="upper left",
    fontsize=8
)

plt.tight_layout()

# Save figure
plt.savefig(
    "Bracken_top15_species_others.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("Plot saved")
