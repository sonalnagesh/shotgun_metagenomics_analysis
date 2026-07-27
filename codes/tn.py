import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import os

# ============================================================
# 1. FIND ALL BRACKEN FILES
# ============================================================

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

# ============================================================
# 2. READ SPECIES-LEVEL BRACKEN DATA
# ============================================================

species_tables = []

for file in bracken_files:

    # Extract sample name
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

    # Keep species-level classifications only
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

# ============================================================
# 3. MERGE ALL SAMPLES
# ============================================================

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

# ============================================================
# 4. READ YOUR METADATA FILE
# ============================================================

metadata = pd.read_csv(
    "total_patient_metadata.csv"
)

# Set the sample ID column as the index
metadata = metadata.set_index(
    "sample_id"
)

# ============================================================
# 5. MATCH SAMPLES BETWEEN BRACKEN AND METADATA
# ============================================================

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

print(
    "Matched samples:",
    len(common_samples)
)

# ============================================================
# 6. IDENTIFY THE OVERALL TOP 15 SPECIES
# ============================================================

# Sum abundance across all samples
total_abundance = (
    merged.sum(
        axis=1
    )
)

# Select the 15 most abundant species
top15_species = (
    total_abundance
    .sort_values(
        ascending=False
    )
    .head(15)
)

print(
    "\nTop 15 species:"
)

print(
    top15_species
)

# ============================================================
# 7. CREATE TOP 15 + OTHERS TABLE
# ============================================================

# Keep only the top 15 species
plot_data = merged.loc[
    top15_species.index
].copy()

# Add all remaining species into "Others"
plot_data.loc[
    "Others"
] = (
    merged.drop(
        top15_species.index
    ).sum()
)

# ============================================================
# 8. SEPARATE TUMOR AND NORMAL SAMPLES
# ============================================================

tumor_samples = metadata[
    metadata["status"]
    .str.lower()
    == "tumor"
].index

normal_samples = metadata[
    metadata["status"]
    .str.lower()
    == "normal"
].index

print(
    "\nTumor samples:",
    len(tumor_samples)
)

print(
    "Normal samples:",
    len(normal_samples)
)

# ============================================================
# 9. CALCULATE MEAN ABUNDANCE
# ============================================================

tumor_mean = (
    plot_data[
        tumor_samples
    ].mean(
        axis=1
    )
)

normal_mean = (
    plot_data[
        normal_samples
    ].mean(
        axis=1
    )
)

# Combine Tumor and Normal
grouped_data = pd.DataFrame({

    "Tumor": tumor_mean,

    "Normal": normal_mean

})

# ============================================================
# 10. CONVERT TO PERCENTAGES
# ============================================================

grouped_data = (
    grouped_data
    .div(
        grouped_data.sum(
            axis=0
        ),
        axis=1
    )
) * 100

# ============================================================
# 11. PLOT STACKED BAR GRAPH
# ============================================================

sns.set_style(
    "white"
)

fig, ax = plt.subplots(
    figsize=(10, 10)
)

# Create colours
colors = sns.color_palette(
    "tab20",
    n_colors=len(
        grouped_data.index
    )
)

# Make Others light grey
others_index = (
    grouped_data.index
    .tolist()
    .index(
        "Others"
    )
)

colors[others_index] = (
    "lightgrey"
)

# Start bottom of bars
bottom = [
    0,
    0
]

# Plot each species
for species, color in zip(
    grouped_data.index,
    colors
):

    values = grouped_data.loc[
        species,
        [
            "Tumor",
            "Normal"
        ]
    ].values

    ax.bar(
        [
            "Tumor",
            "Normal"
        ],
        values,
        bottom=bottom,
        color=color,
        width=0.65,
        label=species,
        edgecolor="white",
        linewidth=0.5
    )

    # Update bottom
    bottom = [
        bottom[i] + values[i]
        for i in range(2)
    ]

# ============================================================
# 12. FORMAT THE GRAPH
# ============================================================

ax.set_ylabel(
    "Mean Relative Abundance (%)",
    fontsize=14
)

ax.set_ylim(
    0,
    100
)

ax.set_title(
    "Top 15 Species",
    fontsize=20,
    fontweight="bold"
)

# Add legend
ax.legend(
    title="",
    bbox_to_anchor=(
        1.02,
        1
    ),
    loc="upper left",
    fontsize=10,
    frameon=False
)

plt.tight_layout()

# ============================================================
# 13. SAVE THE FIGURE
# ============================================================

plt.savefig(
    "Top15_Species_Tumor_vs_Normal.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("Plot saved")
