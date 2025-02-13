import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

class DataApp:
    def __init__(self, root):
        self.root = root
        self.df = None

        # Create GUI components
        self.create_widgets()

    def create_widgets(self):
        # Load dataset button
        tk.Button(self.root, text="Load Dataset", command=self.load_dataset).pack(pady=10)

        # Data preview section
        self.data_preview_label = tk.Label(self.root, text="Data Preview (First 5 Rows)")
        self.data_preview_label.pack(pady=5)

        self.data_preview_text = tk.Text(self.root, height=10, width=80)
        self.data_preview_text.pack(pady=5)

        # Statistics display
        self.statistics_label = tk.Label(self.root, text="Basic Statistics")
        self.statistics_label.pack(pady=5)

        self.statistics_text = tk.Text(self.root, height=5, width=80)
        self.statistics_text.pack(pady=5)

        # Plotting buttons
        tk.Button(self.root, text="Fare vs Age Scatter Plot", command=self.plot_fare_vs_age).pack(pady=5)
        tk.Button(self.root, text="Survival Rate by Class", command=self.plot_survival_by_class).pack(pady=5)

    def load_dataset(self):
        

        try:
          
            # Load the dataset into a DataFrame
            self.df =sns.load_dataset('titanic')

            # Display the first 5 rows
            self.data_preview_text.delete('1.0', tk.END)
            self.data_preview_text.insert(tk.END, self.df.head().to_string())

            # Display basic statistics
            self.show_statistics()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load dataset:\n{e}")

    def show_statistics(self):
        if self.df is not None:
            self.statistics_text.delete('1.0', tk.END)
            # Compute basic statistics
            stats = self.df.describe().loc[['mean', '50%', 'min', 'max']]
            stats.index = ['Mean', 'Median', 'Min', 'Max']
            self.statistics_text.insert(tk.END, stats.to_string())

            # Calculate and display survival rate if 'survived' column exists
            if 'survived' in self.df.columns:
                survival_rate = self.df['survived'].mean() * 100
                self.statistics_text.insert(tk.END, f"\nSurvival Rate: {survival_rate:.2f}%")

    def plot_fare_vs_age(self):
        if self.df is not None and 'fare' in self.df.columns and 'age' in self.df.columns:
            plt.figure(figsize=(8, 6))
            sns.scatterplot(data=self.df, x='age', y='fare')
            plt.title("Fare vs Age")
            plt.show()
        else:
            messagebox.showerror("Error", "Dataset does not contain 'fare' or 'age' columns.")

    def plot_survival_by_class(self):
        if self.df is not None and 'pclass' in self.df.columns and 'survived' in self.df.columns:
            plt.figure(figsize=(8, 6))
            sns.barplot(data=self.df, x='pclass', y='survived')
            plt.title("Survival Rate by Class")
            plt.show()
        else:
            messagebox.showerror("Error", "Dataset does not contain 'pclass' or 'survived' columns.")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Data Analysis GUI")
    app = DataApp(root)
    root.mainloop()
