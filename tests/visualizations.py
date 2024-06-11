from tabulate import tabulate
import matplotlib.pyplot as plt

# Plot f0
def plot_f0(self):
    plt.figure(figsize=(12, 6))
    plt.plot(self.f0[:, 0], self.f0[:, 1], label='Detected F0', color='blue')
    plt.plot(self.reference_f0[:, 0], self.reference_f0[:, 1], label='Reference F0', color='red')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    plt.title('Detected vs Reference F0')
    plt.legend()
    plt.show()
    #plt.savefig('tests/outputs/f0_comparison.png')
    # plt.close()
    
    # Plot MIDI Notes
def plot_MIDI(ref_notes, det_notes):
    plt.figure(figsize=(12, 6))
    for i, (start, end, pitch) in enumerate(ref_notes):
        plt.plot([start, end], [pitch, pitch], color='red', label='Reference MIDI' if i == 0 else "")
    for i, (start, end, pitch) in enumerate(det_notes):
        plt.plot([start, end], [pitch, pitch], color='blue', label='Detected MIDI' if i == 0 else "")
    plt.xlabel('Time (s)')
    plt.ylabel('MIDI Pitch')
    plt.title('Detected vs Reference MIDI Notes')
    plt.legend()
    plt.show()
    # plt.savefig('tests/outputs/midi_comparison.png')
    # plt.close()
        
def plot_precision_recall_curve(recall, precision, label=None, color=None):
    plt.plot(recall, precision, label=label, color=color)

def display_f_measure(f_measure, label):
    print(f"{label} F-measure: {f_measure}")

def visualize_overlap_evaluation(overlap):
    # Plot precision-recall curve for overlap evaluation
    plt.figure(figsize=(8, 6))
    plot_precision_recall_curve(overlap['recall'], overlap['precision'], label='Overlap Precision-Recall Curve', color='blue')
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Overlap Precision-Recall Curve')
    plt.legend()
    plt.show()

    # Display F-measure for overlap evaluation
    display_f_measure(overlap['f_measure'], "Overlap")

    # Display average overlap ratio
    print(f"Average Overlap Ratio: {overlap['avg_overlap_ratio']}")

def visualize_onset_evaluation(onset):
    # Plot precision-recall curve for onset evaluation
    plt.figure(figsize=(8, 6))
    plot_precision_recall_curve(onset['recall'], onset['precision'], label='Onset Precision-Recall Curve', color='green')
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Onset Precision-Recall Curve')
    plt.legend()
    plt.show()

    # Display F-measure for onset evaluation
    display_f_measure(onset['f_measure'], "Onset")

def visualize_offset_evaluation(offset):
    # Plot precision-recall curve for offset evaluation
    plt.figure(figsize=(8, 6))
    plot_precision_recall_curve(offset['recall'], offset['precision'], label='Offset Precision-Recall Curve', color='orange')
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Offset Precision-Recall Curve')
    plt.legend()
    plt.show()

    # Display F-measure for offset evaluation
    display_f_measure(offset['f_measure'], "Offset")

def visualize_assess_notes_results(assessment_results):
    overlap = assessment_results['overlap']
    onset = assessment_results['onset']
    offset = assessment_results['offset']

    visualize_overlap_evaluation(overlap)
    visualize_onset_evaluation(onset)
    visualize_offset_evaluation(offset)
    

def display_assess_notes_metrics(metrics):
    for metric, values in metrics.items():
        headers = [metric.capitalize(), 'Value']
        rows = [[key.capitalize(), f"{value:.4f}"] for key, value in values.items()]
        print(tabulate(rows, headers=headers, tablefmt="grid"))
        print()  # Add a newline between each metric


def display_f0_evaluation_metrics(f0_evaluation):
    headers = ['Metric', 'Value']
    rows = [[metric.capitalize(), f"{value:.4f}"] for metric, value in f0_evaluation.items()]
    print(tabulate(rows, headers=headers, tablefmt="grid"))
