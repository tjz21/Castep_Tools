#!/usr/bin/env python
import argparse
import numpy as np
import matplotlib.pyplot as plt
import subprocess
import glob
import sys

def grep_data(command):
    """Run grep command and return the output as a numpy array."""
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, text=True)
    data = np.array(result.stdout.split(), dtype=float)
    return data

def check_convergence():
    """Check if the optimization has converged by searching for a specific phrase."""
    result = subprocess.run("grep 'BFGS: Geometry optimization completed successfully.' *.castep",
                            shell=True, stdout=subprocess.PIPE, text=True)
    return bool(result.stdout)

def find_castep_file():
    """Find the first .castep file in the current directory."""
    files = glob.glob("*.castep")
    if files:
        return files[0]
    else:
        print("No .castep file found in the current directory.")
        sys.exit(1)

def main(input_file, show_plot):
    print(f"Analyzing file: {input_file}")  # Debugging line
    
    try:
        # Retrieve data using grep commands
        total_energy = grep_data(f"grep 'BFGS: finished iteration' {input_file} | awk '{{print $7}}'")
        delta_E = grep_data(f"grep 'dE/ion' {input_file} | awk '{{print $4}}'")
        F_max = grep_data(f"grep '|F|max' {input_file} | awk '{{print $4}}'")
        R_max = grep_data(f"grep '|dR|max' {input_file} | awk '{{print $4}}'")
        S_max = grep_data(f"grep 'Smax' {input_file} | awk '{{print $4}}'")
        volume_data = grep_data(f"grep 'Current cell volume' {input_file} | awk '{{print $5}}'")[::2]

        # Tolerances for convergence
        delta_E_tol = grep_data(f"grep 'dE/ion' {input_file} | awk '{{print $6}}'")[0]
        F_max_tol = grep_data(f"grep '|F|max' {input_file} | awk '{{print $6}}'")[0]
        R_max_tol = grep_data(f"grep '|dR|max' {input_file} | awk '{{print $6}}'")[0]
        S_max_tol = grep_data(f"grep 'Smax' {input_file} | awk '{{print $6}}'")[0]

        # Check convergence for each criterion
        converged_msg = 'Converged ✓'
        unconverged_msg = 'Not Converged ✗'

        delta_E_converged = converged_msg if delta_E[-1] < delta_E_tol else unconverged_msg
        F_max_converged = converged_msg if F_max[-1] < F_max_tol else unconverged_msg
        R_max_converged = converged_msg if R_max[-1] < R_max_tol else unconverged_msg
        S_max_converged = converged_msg if S_max[-1] < S_max_tol else unconverged_msg

        # Check overall convergence
        overall_converged = check_convergence()

        # Create the x-axis based on the length of the data
        x = np.arange(len(delta_E))

        # Set up a figure with 5 subplots (3 rows, 2 columns)
        fig, axs = plt.subplots(3, 2, figsize=(12, 10))

        # Plot each dataset
        axs[0, 0].plot(x, total_energy, 'o-', label='Total Energy', color='purple')
        axs[0, 0].set_title('Enthalpy')
        axs[0, 0].set_xlabel('Opt. Step.')
        axs[0, 0].set_ylabel('Enthalpy (eV)')
        axs[0, 0].text(0.95, 0.95, f'Final = {total_energy[-1]:.4f}', transform=axs[0, 0].transAxes,
                       fontsize=10, verticalalignment='top', horizontalalignment='right')

        axs[0, 1].plot(np.arange(len(volume_data)), volume_data, 'o-', label='Volume', color='orange')
        axs[0, 1].set_title('Cell Volume')
        axs[0, 1].set_xlabel('Opt. Step.')
        axs[0, 1].set_ylabel(r'Volume (ang$^3$)')
        axs[0, 1].text(0.95, 0.95, f'Final = {volume_data[-1]:.4f}', transform=axs[0, 1].transAxes,
                       fontsize=10, verticalalignment='top', horizontalalignment='right')

        axs[1, 0].plot(x, delta_E, 'o-', label='Delta E', color='b')
        axs[1, 0].set_title('Energy Change')
        axs[1, 0].set_xlabel('Opt. Step.')
        axs[1, 0].set_ylabel('Delta E (eV)')
        axs[1, 0].text(0.95, 0.95, f'Final = {delta_E[-1]:.5f}\nTol = {delta_E_tol:.5f}\n{delta_E_converged}',
                       transform=axs[1, 0].transAxes, fontsize=10, verticalalignment='top', horizontalalignment='right',
                       bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3'))

        axs[1, 1].plot(x, F_max, 'o-', label='F_max', color='r')
        axs[1, 1].set_title('Max Force')
        axs[1, 1].set_xlabel('Opt. Step.')
        axs[1, 1].set_ylabel(r'$F_{\mathrm{max}}$' + ' (eV/ang)')
        axs[1, 1].text(0.95, 0.95, f'Final = {F_max[-1]:.5f}\nTol = {F_max_tol:.5f}\n{F_max_converged}',
                       transform=axs[1, 1].transAxes, fontsize=10, verticalalignment='top', horizontalalignment='right',
                       bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3'))

        axs[2, 0].plot(x, R_max, 'o-', label='R_max', color='g')
        axs[2, 0].set_title('Max Displacement')
        axs[2, 0].set_xlabel('Opt. Step.')
        axs[2, 0].set_ylabel(r'$R_{\mathrm{max}}$' + ' (ang)')
        axs[2, 0].text(0.95, 0.95, f'Final = {R_max[-1]:.5f}\nTol = {R_max_tol:.5f}\n{R_max_converged}',
                       transform=axs[2, 0].transAxes, fontsize=10, verticalalignment='top', horizontalalignment='right',
                       bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3'))

        axs[2, 1].plot(x, S_max, 'o-', label='S_max', color='m')
        axs[2, 1].set_title('Max Stress')
        axs[2, 1].set_xlabel('Opt. Step.')
        axs[2, 1].set_ylabel(r'S$_{\mathrm{max}}$' + ' (GPa)')
        axs[2, 1].text(0.95, 0.95, f'Final = {S_max[-1]:.5f}\nTol = {S_max_tol:.5f}\n{S_max_converged}',
                       transform=axs[2, 1].transAxes, fontsize=10, verticalalignment='top', horizontalalignment='right',
                       bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3'))

        # Overall convergence information
        iterations = len(delta_E)
        convergence_text = (f"Iterations: {iterations}\n"
                            f"Overall Convergence: {'Yes' if overall_converged else 'No'}")

        convergence_color = 'green' if overall_converged else 'red'

        fig.text(0.80, 0.92, convergence_text, ha='center', fontsize=12, color=convergence_color,
                 bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))

        # Adjust layout and add the super title
        plt.tight_layout(rect=[0, 0.05, 1, 0.90])
        fig.suptitle('Castep Cell Optimization', fontsize=16)

        # Show or save the plot
        if show_plot:
            print("Displaying plot...")
            plt.show()
        else:
            print("Saving plot...")
            plt.savefig(f"{input_file}_optimization_plot.png")
            print(f"Plot saved as {input_file}_optimization_plot.png")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot optimization data from a .castep file.')
    parser.add_argument('-f', '--file', type=str, help='Specify the .castep file.')
    parser.add_argument('-s', '--save', action='store_false', help='Saves the plot as a .png file.')
    args = parser.parse_args()

    if args.file:
        input_file = args.file
    else:
        input_file = find_castep_file()

    main(input_file, args.save)

