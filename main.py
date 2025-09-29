#!/usr/bin/env python3
"""
Simulasi Medan Listrik dengan menu (1-4) + simpan gambar + laporan PDF.
Author: ChatGPT for Revario
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime
from fpdf import FPDF
import os
import sys
import textwrap

# ---------------------------
# Konstanta dan util
# ---------------------------
K = 9e9  # gunakan sesuai worksheet: 9 x 10^9 N·m^2/C^2

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def ask_float(prompt, default=None):
    while True:
        try:
            s = input(prompt).strip()
            if s == "" and default is not None:
                return default
            return float(s)
        except ValueError:
            print("Input harus angka. Coba lagi.")

def ask_int(prompt, default=None):
    while True:
        try:
            s = input(prompt).strip()
            if s == "" and default is not None:
                return default
            return int(s)
        except ValueError:
            print("Input harus integer. Coba lagi.")

def ensure_folder(base: Path):
    base.mkdir(parents=True, exist_ok=True)
    return base

def timestamp_str():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

# ---------------------------
# Hitung medan listrik & gaya
# ---------------------------
def e_field_point(charge_q, charge_pos, point_pos):
    # return vektor Ex, Ey dari satu muatan pada titik tertentu
    dx = point_pos[0] - charge_pos[0]
    dy = point_pos[1] - charge_pos[1]
    r2 = dx*dx + dy*dy
    if r2 == 0:
        return (0.0, 0.0)  # akan di-handle luar
    r = np.sqrt(r2)
    Ex = K * charge_q * dx / (r2 * r)  # k*q * (dx / r^3)
    Ey = K * charge_q * dy / (r2 * r)
    return (Ex, Ey)

def e_field_magnitude_formula(q_abs, r):
    # rumus E = k * |Q| / r^2
    if r == 0:
        return float('inf')
    return K * abs(q_abs) / (r**2)

def f_magnitude_formula(Q1, q_uji, r):
    # F = k * |Q1 * q_uji| / r^2
    if r == 0:
        return float('inf')
    return K * abs(Q1 * q_uji) / (r**2)

# ---------------------------
# Plotting helper
# ---------------------------
def generate_plots(charges, out_dir, grid_range_m=5.0, nx=300, ny=300, show_plots=False, test_point=None):
    """
    charges: list of tuples (x, y, q)
    out_dir: Path
    test_point: optional (xu, yu) to mark on plots
    """
    ensure_folder(out_dir)
    # grid
    x = np.linspace(-grid_range_m, grid_range_m, nx)
    y = np.linspace(-grid_range_m, grid_range_m, ny)
    X, Y = np.meshgrid(x, y)
    Ex = np.zeros_like(X)
    Ey = np.zeros_like(Y)
    eps = 1e-12

    for (cx, cy, q) in charges:
        dx = X - cx
        dy = Y - cy
        r2 = dx**2 + dy**2 + eps
        r = np.sqrt(r2)
        Ex += K * q * dx / (r2 * r)
        Ey += K * q * dy / (r2 * r)

    E = np.sqrt(Ex**2 + Ey**2)

    # 1) Quiver
    fig1, ax1 = plt.subplots(figsize=(6,6))
    step = max(1, nx // 25)
    ax1.quiver(X[::step, ::step], Y[::step, ::step],
               Ex[::step, ::step], Ey[::step, ::step], scale=1e11)
    for (cx, cy, q) in charges:
        marker = 'o' if q>0 else 's'
        color = 'red' if q>0 else 'blue'
        ax1.scatter(cx, cy, s=80, marker=marker, color=color)
        ax1.text(cx, cy, f" {q:.3e} C", fontsize=8)
    if test_point:
        ax1.scatter(test_point[0], test_point[1], s=100, marker='*', color='green')
    ax1.set_title("Medan Listrik (Vektor) - Quiver")
    ax1.set_xlabel("x (m)")
    ax1.set_ylabel("y (m)")
    ax1.set_aspect('equal', 'box')
    p1 = out_dir / "quiver.png"
    fig1.tight_layout()
    fig1.savefig(p1, dpi=150)
    if show_plots: fig1.show()
    plt.close(fig1)

    # 2) Streamplot
    fig2, ax2 = plt.subplots(figsize=(6,6))
    lw = 1
    strm = ax2.streamplot(X, Y, Ex, Ey, density=1.2, linewidth=lw)
    for (cx, cy, q) in charges:
        marker = 'o' if q>0 else 's'
        color = 'red' if q>0 else 'blue'
        ax2.scatter(cx, cy, s=80, marker=marker, color=color)
        ax2.text(cx, cy, f" {q:.3e} C", fontsize=8)
    if test_point:
        ax2.scatter(test_point[0], test_point[1], s=100, marker='*', color='green')
    ax2.set_title("Garis Medan Listrik (Streamlines)")
    ax2.set_xlabel("x (m)")
    ax2.set_ylabel("y (m)")
    ax2.set_aspect('equal', 'box')
    p2 = out_dir / "stream.png"
    fig2.tight_layout()
    fig2.savefig(p2, dpi=150)
    if show_plots: fig2.show()
    plt.close(fig2)

    # 3) Heatmap log magnitude
    fig3, ax3 = plt.subplots(figsize=(6,6))
    logE = np.log10(E + 1e-20)
    im = ax3.imshow(logE, extent=(x.min(), x.max(), y.min(), y.max()), origin='lower', cmap='inferno')
    for (cx, cy, q) in charges:
        marker = 'o' if q>0 else 's'
        color = 'red' if q>0 else 'blue'
        ax3.scatter(cx, cy, s=80, marker=marker, color=color)
        ax3.text(cx, cy, f" {q:.3e} C", fontsize=8)
    if test_point:
        ax3.scatter(test_point[0], test_point[1], s=100, marker='*', color='green')
    ax3.set_title("Log10 Magnitudo Medan Listrik")
    ax3.set_xlabel("x (m)")
    ax3.set_ylabel("y (m)")
    ax3.set_aspect('equal', 'box')
    fig3.colorbar(im, ax=ax3, label='log10(|E|)')
    p3 = out_dir / "magnitude_log.png"
    fig3.tight_layout()
    fig3.savefig(p3, dpi=150)
    if show_plots: fig3.show()
    plt.close(fig3)

    return [p1, p2, p3]

# ---------------------------
# PDF report generator (fpdf)
# ---------------------------
class SimplePDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 8, "Laporan Simulasi Medan Listrik", ln=True, align="C")
        self.ln(4)

def create_pdf(report_path: Path, title: str, description: str, inputs_text: str, results_text: str, image_paths):
    pdf = SimplePDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 6, f"{title}\n\n", align="L")
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 6, "Deskripsi:\n" + description + "\n\n")
    pdf.multi_cell(0, 6, "Input / Parameter:\n" + inputs_text + "\n\n")
    pdf.multi_cell(0, 6, "Hasil perhitungan:\n" + results_text + "\n\n")

    for img in image_paths:
        pdf.add_page()
        pdf.set_font("Arial", "B", 10)
        pdf.cell(0, 6, f"Gambar: {img.name}", ln=True)
        # Fit image to page with margin
        w = 180
        h = 0
        pdf.image(str(img), x=15, y=30, w=w, h=h)
    pdf.output(str(report_path))

# ---------------------------
# Menu actions
# ---------------------------
def menu_interaksi(output_base, unit_scale):
    """
    Menu 1: Interaksi Muatan (dua muatan; muatan 1 di (0,0), muatan2 di jarak sumbu x)
    """
    print("\n-- Menu: Interaksi Muatan --")
    Q1 = ask_float("Masukkan nilai muatan pertama Q1 (C, +/-): ")
    # Q1 at (0,0)
    print("Muatan pertama akan ditempatkan di (0,0).")
    jarak = ask_float("Masukkan jarak muatan kedua dari (0,0) sepanjang sumbu x (positif ke kanan) dalam satuan yang sama: ")
    arah = input("Arah (L/R) atau tekan Enter as R: ").strip().upper()
    if arah == "L":
        x2 = -abs(jarak) * unit_scale
    else:
        x2 = abs(jarak) * unit_scale
    y2 = 0.0
    Q2 = ask_float("Masukkan nilai muatan kedua Q2 (C, +/-): ")

    charges = [(0.0, 0.0, Q1), (x2, y2, Q2)]
    tdir = output_base / f"hasil_simulasi_{timestamp_str()}_menu1"
    ensure_folder(tdir)

    # compute some representative numbers: distance between sources
    d = np.sqrt((x2 - 0.0)**2 + (y2 - 0.0)**2)
    # compute E at midpoint and at some sample points
    sample_point = ( (0.0 + x2)/2.0, 0.0 )
    Ex1, Ey1 = e_field_point(Q1, (0.0,0.0), sample_point)
    Ex2, Ey2 = e_field_point(Q2, (x2,y2), sample_point)
    Etot_x = Ex1 + Ex2
    Etot_y = Ey1 + Ey2
    Etot = np.sqrt(Etot_x**2 + Etot_y**2)

    # generate plots
    imgs = generate_plots(charges, tdir, grid_range_m=max(2.0, abs(x2)*2 + 1.0), test_point=sample_point)

    # create text blocks for pdf
    title = "Interaksi Muatan - Dua Muatan"
    description = "Simulasi interaksi antara dua muatan titik. Muatan 1 di (0,0), muatan 2 pada jarak yang ditentukan di sumbu-x."
    inputs_text = f"Q1 = {Q1:.3e} C at (0.0, 0.0)\nQ2 = {Q2:.3e} C at ({x2:.3f}, {y2:.3f}) m\nJarak antar muatan = {d:.4f} m"
    results_text = f"Medan listrik di titik tengah ({sample_point[0]:.4f}, {sample_point[1]:.4f}) m:\n"
    results_text += f" E1 = ({Ex1:.3e}, {Ey1:.3e}) N/C\n E2 = ({Ex2:.3e}, {Ey2:.3e}) N/C\n E_total = ({Etot_x:.3e}, {Etot_y:.3e}) N/C, |E| = {Etot:.3e} N/C\n"
    # pdf
    pdf_path = tdir / "laporan_interaksi.pdf"
    create_pdf(pdf_path, title, description, inputs_text, results_text, imgs)
    print(f"Selesai. Hasil disimpan di folder: {tdir}")
    print(f"Laporan PDF: {pdf_path}")

def menu_medan_garis(output_base, unit_scale):
    """
    Menu 2: Medan Listrik & Garis Medan (1 atau 2 muatan)
    """
    print("\n-- Menu: Medan Listrik & Garis Medan --")
    mode = input("Pilihan: (1) Satu muatan, (2) Dua muatan [default 2]: ").strip()
    if mode == "" or mode == "2":
        # two charges
        Q1 = ask_float("Masukkan Q1 (C) untuk muatan pertama di (0,0): ")
        jarak = ask_float("Masukkan jarak muatan kedua dari (0,0) sepanjang sumbu x (satuan Anda): ")
        arah = input("Arah (L/R) atau Enter as R: ").strip().upper()
        if arah == "L":
            x2 = -abs(jarak) * unit_scale
        else:
            x2 = abs(jarak) * unit_scale
        Q2 = ask_float("Masukkan Q2 (C): ")
        charges = [(0.0, 0.0, Q1), (x2, 0.0, Q2)]
    else:
        Q1 = ask_float("Masukkan Q1 (C) untuk muatan di (0,0): ")
        charges = [(0.0, 0.0, Q1)]

    tdir = output_base / f"hasil_simulasi_{timestamp_str()}_menu2"
    ensure_folder(tdir)
    imgs = generate_plots(charges, tdir, grid_range_m=5.0, test_point=None)

    title = "Medan Listrik & Garis Medan"
    description = "Visualisasi medan listrik (vektor, streamlines, heatmap) dari konfigurasi muatan yang diberikan."
    inputs_text = "\n".join([f"Charge {i+1}: pos=({c[0]:.3f}, {c[1]:.3f}) m, q={c[2]:.3e} C" for i,c in enumerate(charges)])
    results_text = "Gambar visualisasi medan telah disimpan."
    pdf_path = tdir / "laporan_medan_garis.pdf"
    create_pdf(pdf_path, title, description, inputs_text, results_text, imgs)
    print(f"Selesai. Hasil disimpan di folder: {tdir}")
    print(f"Laporan PDF: {pdf_path}")

def menu_analisis_kuantitatif(output_base, unit_scale):
    """
    Menu 3: Analisis Kuantitatif (E dan F untuk titik gaya + titik sensor)
    Input muatan dalam nanoCoulomb (nC).
    """
    print("\n-- Menu: Analisis Kuantitatif (Hukum Coulomb & Medan) --")
    print("⚡ Catatan: Semua input muatan dalam satuan nanoCoulomb (nC).")
    print("   Contoh: -6 artinya -6 nC = -6e-9 C\n")

    # 1) Muatan sumber
    Q1_nC = ask_float("Masukkan muatan sumber Q1 (nC) di (0,0): ")
    Q1 = Q1_nC * 1e-9  # konversi ke Coulomb

    # 2) Titik gaya
    print("\n=== Input Titik Gaya ===")
    gaya_points = []
    while True:
        s = input("Titik gaya (format: x y / done): ").strip()
        if s.lower() == "done":
            break
        try:
            x, y = map(float, s.split())
            x *= unit_scale
            y *= unit_scale
            q_nC = ask_float("  Masukkan muatan uji q di titik ini (nC): ")
            q_uji = q_nC * 1e-9
            gaya_points.append((x, y, q_uji, q_nC))
        except ValueError:
            print("⚠️ Format salah! Harus: x y (contoh: 0.5 0)")

    # 3) Titik sensor
    print("\n=== Input Titik Sensor Medan ===")
    sensor_points = []
    while True:
        s = input("Titik sensor (format: x y / done): ").strip()
        if s.lower() == "done":
            break
        try:
            x, y = map(float, s.split())
            x *= unit_scale
            y *= unit_scale
            sensor_points.append((x, y))
        except ValueError:
            print("⚠️ Format salah! Harus: x y (contoh: 1.5 0)")

    if not gaya_points and not sensor_points:
        print("⚠️ Tidak ada titik uji dimasukkan. Batal.")
        return

    # 4) Perhitungan
    results_lines = []
    charges = [(0.0, 0.0, Q1)]
    tdir = output_base / f"hasil_simulasi_{timestamp_str()}_menu3"
    ensure_folder(tdir)

    # --- Titik gaya ---
    if gaya_points:
        results_lines.append("=== HASIL TITIK GAYA ===")
        for i, (xu, yu, q_uji, q_nC) in enumerate(gaya_points, start=1):
            r = np.sqrt(xu**2 + yu**2)
            E_magn = e_field_magnitude_formula(Q1, r)
            F_magn = f_magnitude_formula(Q1, q_uji, r)
            results_lines.append(
                f"Titik Gaya {i}: ({xu:.2g}, {yu:.2g}) m, q_uji={q_nC} nC\n"
                f"  r = {r:.2g} m\n"
                f"  |E| = {E_magn:.3g} N/C\n"
                f"  |F| = {F_magn:.3g} N\n"
            )

    # --- Titik sensor ---
    if sensor_points:
        results_lines.append("\n=== HASIL TITIK SENSOR ===")
        for j, (xu, yu) in enumerate(sensor_points, start=1):
            r = np.sqrt(xu**2 + yu**2)
            E_magn = e_field_magnitude_formula(Q1, r)
            results_lines.append(
                f"Titik Sensor {j}: ({xu:.2g}, {yu:.2g}) m\n"
                f"  r = {r:.2g} m\n"
                f"  |E| = {E_magn:.3g} N/C\n"
            )

    # 5) Plot
    imgs = generate_plots(charges, tdir, grid_range_m=5.0)
    fig, ax = plt.subplots(figsize=(6,6))
    if gaya_points:
        xs, ys = zip(*[(p[0], p[1]) for p in gaya_points])
        ax.scatter(xs, ys, c="green", marker="*", s=100, label="Titik Gaya")
    if sensor_points:
        xs, ys = zip(*sensor_points)
        ax.scatter(xs, ys, c="orange", marker="x", s=100, label="Titik Sensor")
    ax.scatter(0,0, c="red", marker="o", s=80, label="Q1")
    ax.set_title("Titik Gaya & Sensor Medan")
    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")
    ax.legend()
    extra_img = tdir / "titik_uji.png"
    fig.savefig(extra_img, dpi=150)
    plt.close(fig)
    imgs.append(extra_img)

    # 6) PDF
    title = "Analisis Kuantitatif - Titik Gaya & Sensor"
    description = ("Menghitung medan listrik dan gaya di titik uji.\n"
                   "- Titik gaya: ada q_uji, dihitung E & F.\n"
                   "- Titik sensor: hanya dihitung E.")
    inputs_text = f"Q1 = {Q1_nC} nC di (0,0)\n"
    if gaya_points:
        inputs_text += "\nTitik gaya:\n" + "\n".join(
            [f"  ({x:.2g}, {y:.2g}) m, q_uji={q_nC} nC"
             for x, y, q_uji, q_nC in gaya_points])
    if sensor_points:
        inputs_text += "\nTitik sensor:\n" + "\n".join(
            [f"  ({x:.2g}, {y:.2g}) m" for x,y in sensor_points])

    results_text = "\n".join(results_lines)
    pdf_path = tdir / "laporan_analisis_kuantitatif.pdf"
    create_pdf(pdf_path, title, description, inputs_text, results_text, imgs)

    print(f"Selesai. Hasil disimpan di folder: {tdir}")
    print(f"Laporan PDF: {pdf_path}")



def menu_superposisi(output_base, unit_scale):
    """
    Menu 4: Superposisi medan listrik (dua muatan; posisi simetris -d dan +d)
    """
    print("\n-- Menu: Superposisi Medan Listrik --")
    Q1 = ask_float("Masukkan muatan Q1 (C) (akan ditempatkan di x = -d): ")
    Q2 = ask_float("Masukkan muatan Q2 (C) (akan ditempatkan di x = +d): ")
    d = ask_float("Masukkan jarak d (meter atau satuan Anda) -> muatan akan pada -d dan +d: ")
    x1 = -abs(d) * unit_scale
    x2 = +abs(d) * unit_scale
    sensor_x = ask_float("Masukkan posisi sensor pada sumbu-x (default 0): ") if input("Ingin ganti posisi sensor? (y/N): ").strip().lower() == 'y' else 0.0
    sensor_y = 0.0
    sensor_pos = (sensor_x*unit_scale, sensor_y)

    charges = [(x1, 0.0, Q1), (x2, 0.0, Q2)]
    # Hitung E vektor di sensor
    Ex_tot, Ey_tot = 0.0, 0.0
    for (cx, cy, q) in charges:
        ex, ey = e_field_point(q, (cx, cy), sensor_pos)
        Ex_tot += ex
        Ey_tot += ey
    Etot = np.sqrt(Ex_tot**2 + Ey_tot**2)
    tdir = output_base / f"hasil_simulasi_{timestamp_str()}_menu4"
    ensure_folder(tdir)
    imgs = generate_plots(charges, tdir, grid_range_m=max(2.0, abs(d)*2 + 1.0), test_point=sensor_pos)

    title = "Superposisi Medan Listrik (dua muatan)"
    description = "Menghitung medan listrik total di titik sensor sebagai superposisi vektor dari dua muatan."
    inputs_text = f"Q1 = {Q1:.3e} C at ({x1:.3f}, 0.0) m\nQ2 = {Q2:.3e} C at ({x2:.3f}, 0.0) m\nSensor: ({sensor_pos[0]:.4f}, {sensor_pos[1]:.4f}) m"
    results_text = f"E_total vector = ({Ex_tot:.3e}, {Ey_tot:.3e}) N/C\n|E_total| = {Etot:.3e} N/C"
    pdf_path = tdir / "laporan_superposisi.pdf"
    create_pdf(pdf_path, title, description, inputs_text, results_text, imgs)
    print(f"Selesai. Hasil disimpan di folder: {tdir}")
    print(f"Laporan PDF: {pdf_path}")

# ---------------------------
# Main program
# ---------------------------
def main():
    clear_terminal()
    print("=== Program Simulasi Medan Listrik ===")
    print("Pilih satuan posisi input:")
    one_unit = input("Masukkan 'm' untuk meter atau 'cm' untuk centimeter [m/cm, default m]: ").strip().lower()
    if one_unit == "cm":
        unit_scale = 0.01
    else:
        unit_scale = 1.0

    base_out = Path.cwd() / "hasil_simulasi"
    ensure_folder(base_out)

    while True:
        print("\nMenu utama:")
        print("1) Interaksi Muatan (dua muatan, Q1 di (0,0))")
        print("2) Medan Listrik & Garis Medan (visualisasi 1 atau 2 muatan)")
        print("3) Analisis Kuantitatif (hitung E dan F di titik uji)")
        print("4) Superposisi Medan Listrik (dua muatan, hitung E total di sensor)")
        print("0) Keluar")
        choice = input("Pilih menu (0-4): ").strip()
        if choice == "0":
            print("Keluar. Sampai jumpa!")
            break
        elif choice == "1":
            menu_interaksi(base_out, unit_scale)
        elif choice == "2":
            menu_medan_garis(base_out, unit_scale)
        elif choice == "3":
            menu_analisis_kuantitatif(base_out, unit_scale)
        elif choice == "4":
            menu_superposisi(base_out, unit_scale)
        else:
            print("Pilihan tidak dikenal. Coba lagi.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nDijeda oleh user. Keluar.")
        sys.exit(0)
