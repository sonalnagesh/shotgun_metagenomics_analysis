import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import os

# 1. Read all Bracken files
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

# 2. Read species-level abundance data
species_tables = []

for file in bracken_files:

    # Get sample name
    sample = os.path.basename(
        file
    ).replace(
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

# 3. Merge all samples
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

print(
    "Merged table:",
    merged.shape
)

# 4. Read metadata file
metadata = pd.read_csv(
    "total_patient_metadata.csv"
)

# Make sure your metadata has columns:
# sample_id
# sex

# Set sample_id as index
metadata = metadata.set_index(
    "sample_id"
)

# Keep only samples present
# in both files
common_samples = (
    merged.columns
    .intersection(
        metadata.index
    )
)

merged = merged[
    common_samples
]

metadata = metadata.loc[
    common_samples
]

# 5. Calculate total abundance
#    across all samples
total_abundance = (
    merged.sum(
        axis=1
    )
)

# Select the top 15 species
top15 = (
    total_abundance
    .sort_values(
        ascending=False
    )
    .head(15)
)

# 6. Combine all remaining species
#    into Others

others = (
    total_abundance
    .drop(
        top15.index
    )
    .sum()
)

# Create table containing
# top 15 species
plot_data = merged.loc[
    top15.index
].copy()

# Add Others
plot_data.loc[
    "Others"
] = (
    merged.drop(
        top15.index
    ).sum()
)

# 7. Calculate mean abundance
#    for Male and Female

male_samples = metadata[
    metadata["sex"] == "Male"
].index

female_samples = metadata[
    metadata["sex"] == "Female"
].index

male_abundance = (
    plot_data[
        male_samples
    ].mean(
        axis=1
    )
)

female_abundance = (
    plot_data[
        female_samples
    ].mean(
        axis=1
    )
)

# Combine Male and Female
plot_data = pd.DataFrame({

    "Male": male_abundance,

    "Female": female_abundance

})

# 8. Convert to percentages
plot_data = (
    plot_data
    .div(
        plot_data.sum(
            axis=0
        ),
        axis=1
    )
) * 100

# 9. Plot
sns.set_style(
    "white"
)

fig, ax = plt.subplots(
    figsize=(8, 8)
)

# Create colours
colors = sns.color_palette(
    "tab20",
    n_colors=len(
        plot_data.index
    )
)

# Make Others grey
colors = list(
    colors
)

colors[
    plot_data.index
    .tolist()
    .index(
        "Others"
    )
] = "lightgrey"

# Start at zero
bottom = [
    0,
    0
]

# Plot each species
for species, color in zip(
    plot_data.index,
    colors
):

    values = plot_data.loc[
        species,
        [
            "Male",
            "Female"
        ]
    ].values

    ax.bar(
        [
            "Male",
            "Female"
        ],
        values,
        bottom=bottom,
        color=color,
        width=0.65,
        label=species
    )

    # Update bottom
    bottom = [
        bottom[i] + values[i]
        for i in range(2)
    ]

# 10. Format graph
ax.set_ylabel(
    "Relative abundance (%)",
    fontsize=12
)

ax.set_ylim(
    0,
    100
)

ax.set_title(
    "Top 15 Species Abundance\nMale vs Female",
    fontsize=14
)

# Add legend
ax.legend(
    bbox_to_anchor=(
        1.05,
        1
    ),
    loc="upper left",
    fontsize=8,
    frameon=False
)

plt.tight_layout()

# Save figure
plt.savefig(
    "Top15_Species_Male_vs_Female.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

