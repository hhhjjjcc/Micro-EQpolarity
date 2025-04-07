import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Load the CSV file
file_path = "./training_log_90.csv"
df = pd.read_csv(file_path)

# Step 2: Plot and save Training Loss and Validation Loss curves
fig, ax = plt.subplots(figsize=(10, 6))  # Increase figure size
ax.plot(df['epoch'], df['loss'], 'r--', label='Training Loss')  # Red dashed line for Training Loss
ax.plot(df['epoch'], df['val_loss'], 'k--', label='Validation Loss')  # Black dashed line for Validation Loss

ax.set_xlabel('Epoch', fontsize=30)
ax.set_ylabel('Loss', fontsize=30)
ax.set_title('Training and Validation Loss', fontsize=30)
ax.tick_params(axis='both', labelsize=24)
ax.legend(fontsize=24)
ax.grid(True)

# Adjust layout to remove extra margins
plt.tight_layout()
plt.savefig('training_validation_loss.png', dpi=300, bbox_inches='tight')  # Save without extra margins
plt.show()

# Step 3: Plot and save Training Accuracy and Validation Accuracy curves
fig, ax = plt.subplots(figsize=(10, 6))  # Increase figure size
ax.plot(df['epoch'], df['acc'] * 100, 'r--', label='Training Accuracy')  # Red dashed line for Training Accuracy
ax.plot(df['epoch'], df['val_acc'] * 100, 'k--', label='Validation Accuracy')  # Black dashed line for Validation Accuracy

ax.set_xlabel('Epoch', fontsize=30)
ax.set_ylabel('Accuracy (%)', fontsize=30)
ax.set_title('Training and Validation Accuracy', fontsize=30)
ax.tick_params(axis='both', labelsize=24)
ax.legend(fontsize=24)
ax.grid(True)

# Adjust layout to remove extra margins
plt.tight_layout()
plt.savefig('training_validation_accuracy.png', dpi=300, bbox_inches='tight')  # Save without extra margins
plt.show()
