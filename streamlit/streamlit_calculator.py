import streamlit as st

st.set_page_config(page_title="Mini Calculator", page_icon="🧮", layout="centered")

st.title("Mini Calculator 🧮")

# Input fields
num1 = st.number_input("Enter first number", value=0.0, format="%.4f")
num2 = st.number_input("Enter second number", value=0.0, format="%.4f")

# Operation
operation = st.radio("Choose operation", ["Add (+)", "Subtract (-)", "Multiply (×)", "Divide (÷)"])

# Calculate
if st.button("Calculate"):
    try:
        if operation.startswith("Add"):
            result = num1 + num2
        elif operation.startswith("Subtract"):
            result = num1 - num2
        elif operation.startswith("Multiply"):
            result = num1 * num2
        elif operation.startswith("Divide"):
            result = num1 / num2

        # Show result
        st.success(f"Result = {result}")
    except ZeroDivisionError:
        st.error("Error: Division by zero")
