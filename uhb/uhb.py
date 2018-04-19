import numpy as np
import matplotlib.pyplot as plt
import json

import soil


def plot_stiffnesses(burial_depths, results, soil_type):

    fig, ax = plt.subplots()

    for stiffness in ["K_a", "K_l", "K_vu", "K_vb"]:
        ax.plot(
            burial_depths,
            [results[soil_type][b][stiffness] for b in burial_depths],
            marker="o",
            label=stiffness,
        )

    ax.set_title(f"Soil Stiffnesses vs. Burial Depth\n({soil_type.title()})")
    ax.set_xlabel("Burial Depth [m]")
    ax.set_ylabel("Stiffness [N/m]")
    ax.grid()
    ax.legend()
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    fig.savefig(f"outputs/{soil_type}.png")


if __name__ == "__main__":
    D = 0.1731
    f = 0.6

    soils = {
        "dense sand": {"c": 0, "phi_s": 32, "gamma": 18000},
        "soft clay": {"c": 0.6, "phi_s": 0, "gamma": 18000},
    }

    burial_depths = np.arange(0.1, 0.6, 0.1)

    results = {}

    for soil_case in ["dense sand", "soft clay"]:
        print(soil_case)
        results[soil_case] = {}
        for b in burial_depths:
            H = b + D / 2
            T_u = soil.Tu(
                D,
                H,
                soils[soil_case]["c"],
                f,
                soils[soil_case]["phi_s"],
                soils[soil_case]["gamma"],
            )
            delta_t = soil.Delta_t(soil_case)
            P_u = soil.Pu(
                soils[soil_case]["c"],
                H,
                D,
                soils[soil_case]["phi_s"],
                soils[soil_case]["gamma"],
            )
            delta_p = soil.Delta_p(H, D)
            Q_u = soil.Qu(
                soils[soil_case]["phi_s"],
                soils[soil_case]["c"],
                D,
                soils[soil_case]["gamma"],
                H,
            )
            delta_qu = soil.Delta_qu(soil_case, H, D)
            Q_d = soil.Qd(
                soils[soil_case]["phi_s"],
                soils[soil_case]["c"],
                D,
                soils[soil_case]["gamma"],
                H,
            )
            delta_qd = soil.Delta_qd(soil_case, D)

            results[soil_case][b] = {
                "T_u": T_u,
                "delta_t": delta_t,
                "K_a": T_u / delta_t,
                "P_u": P_u,
                "delta_p": delta_p,
                "K_l": P_u / delta_p,
                "Q_u": Q_u,
                "delta_qu": delta_qu,
                "K_vu": Q_u / delta_qu,
                "Q_d": Q_d,
                "delta_qd": delta_qd,
                "K_vb": Q_d / delta_qd,
            }

        print(
            soil.DepthEquilibrium(
                soils[soil_case]["phi_s"],
                soils[soil_case]["c"],
                D,
                soils[soil_case]["gamma"],
                soil_case,
            )
        )

    with open("outputs/soil_stiffnesses.json", "w") as outfile:
        json.dump(results, outfile, indent=4)

    plot_stiffnesses(burial_depths, results, "soft clay")
    plot_stiffnesses(burial_depths, results, "dense sand")
