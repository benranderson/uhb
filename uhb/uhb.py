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

                soil_weight = results[soil][burial_depth]["soil weight"]

                o.write(f"Burial depth: {burial_depth:.2f} m\n")
                o.write(f"PUDL, 1, 2, -{soil_weight:.2f}\n\n")
                o.write("Vertical up (Feed-in zone and intermediate zone)\n")
                Q_u = results[soil][burial_depth]["Q_u"]
                delta_qu = results[soil][burial_depth]["delta_qu"]
                o.write(f"RC, 1, {delta_qu:.5f}, {Q_u:.3E}, 100, {Q_u:.3E}\n")

                o.write("Lateral (Feed-in zone)\n")
                P_u = results[soil][burial_depth]["P_u"]
                delta_p = results[soil][burial_depth]["delta_p"]
                o.write(f"RC, 2, {delta_p:.5f}, {P_u:.3E}, 100, {P_u:.3E}\n")

                o.write("Vertical down (Feed-in zone)\n")
                Q_d = results[soil][burial_depth]["Q_d"]
                delta_qd = results[soil][burial_depth]["delta_qd"]
                o.write(f"RC, 3, {delta_qd:.5f}, {Q_d:.3E}, 100, {Q_d:.3E}\n")

                o.write("Lateral (Imperfection)\n")
                o.write(f"RC, 4, {delta_p:.5f}, {P_u:.3E}, 100, {P_u:.3E}\n")

                o.write("Vertical up (Imperfection)\n")
                o.write(
                    f"RC, 5, {delta_qu:.5f}, {Q_u - soil_weight:.3E}, {burial_depth:.5f}, -{soil_weight:.3E}, 100, -{soil_weight:.3E}\n"
                )

                o.write("Vertical down (Imperfection)\n")
                o.write(f"RC, 6, {delta_qd:.5f}, {Q_d:.3E}, 100, {Q_d:.3E}\n")

                o.write("Axial (Imperfection)\n")
                T_u = results[soil][burial_depth]["T_u"]
                delta_t = results[soil][burial_depth]["delta_t"]
                o.write(f"RC, 7, {delta_t:.5f}, {T_u:.3E}, 100, {T_u:.3E}\n")

                o.write("Axial (Intermediate)\n")
                o.write(f"RC, 8, {delta_t:.5f}, {T_u:.3E}, 100, {T_u:.3E}\n")

                o.write("Axial (Feed-in zone)\n")
                o.write(f"RC, 9, {delta_t:.5f}, {T_u:.3E}, 100, {T_u:.3E}\n")

                o.write("Vertical down (Backfill down resistance)\n")
                o.write(f"RC, 10, {delta_qd:.5f}, {Q_d:.3E}, 100, {Q_d:.3E}\n\n")

    print("Soil stiffnesses written to outputs/stiffnesses.txt")


if __name__ == "__main__":
    D = 0.1731
    f = 0.6

    soils = {
        "dense sand": {"c": 0, "phi_s": 32, "gamma": 18000},
        "soft clay": {"c": 0.6, "phi_s": 0, "gamma": 18000},
    }

    burial_depths = np.arange(0.25, 1.25, 0.25)

    results = {}

    for soil_case in ["dense sand", "soft clay"]:
        results[soil_case] = {}
        c = soils[soil_case]["c"]
        phi_s = soils[soil_case]["phi_s"]
        gamma = soils[soil_case]["gamma"]

        for b in burial_depths:
            H = b + D / 2
            T_u = soil.Tu(D, H, c, f, phi_s, gamma)
            delta_t = soil.Delta_t(soil_case)
            P_u = soil.Pu(c, H, D, phi_s, gamma)
            delta_p = soil.Delta_p(H, D)
            Q_u = soil.Qu(phi_s, c, D, gamma, H)
            delta_qu = soil.Delta_qu(soil_case, H, D)
            Q_d = soil.Qd(phi_s, c, D, gamma, H)
            delta_qd = soil.Delta_qd(soil_case, D)

            results[soil_case][b] = {
                "soil weight": soil.soil_weight(gamma, b, D),
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
