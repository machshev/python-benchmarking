from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def plot(dir: Path):
    data = pd.DataFrame()

    for file in dir.glob("*.full.csv"):
        name = file.stem.split(".")[0]
        df = pd.read_csv(file, converters={"ctype": str})
        df["alg"] = name

        data = pd.concat([data, df])

    algorithms = data["alg"].unique()
    loads = data["load"].unique()
    ctypes = data["ctype"].unique()

    fig, axs = plt.subplots(len(algorithms), len(loads), layout="constrained")

    for j, alg in enumerate(algorithms):
        for i, load in enumerate(loads):
            ax = axs[j, i]
            ax.set_title(f"{alg} {load}")
            ax.set_xlabel("workers")
            ax.set_ylabel("runtime (s)")

            for ctype in ctypes:
                filtered = data[
                    (data["alg"] == alg)
                    & (data["load"] == load)
                    & (data["ctype"] == ctype)
                ]

                ax.scatter(
                    filtered["workers"],
                    filtered["mean"],
                    label=f"{alg}_{load}_{ctype}",
                )

    plt.show()


if __name__ == "__main__":
    plot(Path.cwd())
