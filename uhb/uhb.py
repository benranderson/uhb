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


def write_stiffnesses_to_file(results):
    with open(f"outputs/stiffnesses.txt", "w") as o:
        o.write(f"STIFFNESSES\n")
        for soil in results:
            o.write(f"\nSoil type: {soil}\n")
            o.write(f"{'-'*(11+len(soil))}\n\n")
            for burial_depth in results[soil]:
                o.write(f"Burial depth: {burial_depth:.1f} m\n\n")
                o.write("Axial\n")
                T_u = results[soil][burial_depth]["T_u"]
                delta_t = results[soil][burial_depth]["delta_t"]
                K_a = results[soil][burial_depth]["K_a"]
                o.write(f"{T_u:.6f}, {delta_t:.6f}, {K_a:.6f}\n")
                o.write("Lateral\n")
                P_u = results[soil][burial_depth]["P_u"]
                delta_p = results[soil][burial_depth]["delta_p"]
                K_l = results[soil][burial_depth]["K_l"]
                o.write(f"{P_u:.6f}, {delta_p:.6f}, {K_l:.6f}\n")
                o.write("Vertical Uplift\n")
                Q_u = results[soil][burial_depth]["Q_u"]
                delta_qu = results[soil][burial_depth]["delta_qu"]
                K_vu = results[soil][burial_depth]["K_vu"]
                o.write(f"{Q_u:.6f}, {delta_qu:.6f}, {K_vu:.6f}\n")
                o.write("Vertical Bearing\n")
                Q_d = results[soil][burial_depth]["Q_d"]
                delta_qd = results[soil][burial_depth]["delta_qd"]
                K_vb = results[soil][burial_depth]["K_vb"]
                o.write(f"{Q_d:.6f}, {delta_qd:.6f}, {K_vb:.6f}\n\n")


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

    write_stiffnesses_to_file(results)

# print(
#     soil.DepthEquilibrium(
#         soils[soil_case]["phi_s"],
#         soils[soil_case]["c"],
#         D,
#         soils[soil_case]["gamma"],
#         soil_case,
#     )
# )

# with open("outputs/soil_stiffnesses.json", "w") as outfile:
#     json.dump(results, outfile, indent=4)

# plot_stiffnesses(burial_depths, results, "soft clay")
# plot_stiffnesses(burial_depths, results, "dense sand")
