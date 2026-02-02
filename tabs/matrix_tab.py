import streamlit as st
from funmaio.parser import text_to_numpy, numpy_to_text
from funmaio.operations import multiply, inverse, add, subtract, transpose, determinant, eigenvalues, rank
import json


def export_result(result, format_type, operation_name):
    if format_type == "CSV":
        csv_data = "\n".join([";".join(map(str, row)) for row in result])
        return csv_data, f"{operation_name}_result.csv", "text/csv"
    elif format_type == "JSON":
        json_data = json.dumps(result.tolist(), indent=2)
        return json_data, f"{operation_name}_result.json", "application/json"
    elif format_type == "TXT":
        txt_data = numpy_to_text(result, decimals=st.session_state.get('decimal_places', 4))
        return txt_data, f"{operation_name}_result.txt", "text/plain"


def show():
    st.header("Matrix Operations")
    st.write("Perform basic mathematical operations on matrices.")

    operation = st.selectbox(
        "Select operation:",
        ["Matrix Multiplication", "Matrix Addition", "Matrix Subtraction",
         "Inverse Matrix", "Transpose", "Determinant", "Eigenvalues", "Matrix Rank"]
    )

    if operation in ["Matrix Multiplication", "Matrix Addition", "Matrix Subtraction"]:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Matrix A")
            matrix_a = st.text_area(
                "Enter matrix A (separate rows with newline, values with spaces):",
                "1 2 3\n4 5 6\n7 8 9",
                height=150,
                key="matrix_a"
            )

        with col2:
            st.subheader("Matrix B")
            matrix_b = st.text_area(
                "Enter matrix B (separate rows with newline, values with spaces):",
                "9 8 7\n6 5 4\n3 2 1",
                height=150,
                key="matrix_b"
            )

        button_label = operation.split()[1]
        if st.button(button_label, type="primary"):
            a = text_to_numpy(matrix_a)
            b = text_to_numpy(matrix_b)

            if isinstance(a, str) or isinstance(b, str):
                st.error("Invalid matrix format")
            else:
                if operation == "Matrix Multiplication":
                    result = multiply(a, b)
                elif operation == "Matrix Addition":
                    result = add(a, b)
                else:
                    result = subtract(a, b)

                if isinstance(result, str):
                    st.error(result)
                else:
                    st.success("Operation completed successfully!")
                    st.subheader("Result:")
                    decimals = st.session_state.get('decimal_places', 2)
                    st.code(numpy_to_text(result, decimals=decimals))

                    st.session_state['last_result'] = result
                    st.session_state['last_operation'] = operation

                    st.markdown("### Export Result")
                    col1, col2, col3 = st.columns(3)
                    export_formats = st.session_state.get('export_formats', ['CSV', 'JSON', 'TXT'])

                    if 'CSV' in export_formats:
                        with col1:
                            data, filename, mime = export_result(result, "CSV", operation.replace(" ", "_"))
                            st.download_button("📥 Export CSV", data, filename, mime)

                    if 'JSON' in export_formats:
                        with col2:
                            data, filename, mime = export_result(result, "JSON", operation.replace(" ", "_"))
                            st.download_button("📥 Export JSON", data, filename, mime)

                    if 'TXT' in export_formats:
                        with col3:
                            data, filename, mime = export_result(result, "TXT", operation.replace(" ", "_"))
                            st.download_button("📥 Export TXT", data, filename, mime)

    elif operation == "Inverse Matrix":
        st.subheader("Matrix to Invert")
        matrix_input = st.text_area(
            "Enter square matrix (separate rows with newline, values with spaces):",
            "4 7\n2 6",
            height=150,
            key="matrix_inverse"
        )

        if st.button("Calculate Inverse", type="primary"):
            a = text_to_numpy(matrix_input)

            if isinstance(a, str):
                st.error("Invalid matrix format")
            else:
                result = inverse(a)
                if isinstance(result, str):
                    st.error(result)
                else:
                    st.success("Inverse matrix calculated successfully!")
                    st.subheader("Result:")
                    decimals = st.session_state.get('decimal_places', 4)
                    st.code(numpy_to_text(result, decimals=decimals))

                    st.session_state['last_result'] = result
                    st.session_state['last_operation'] = operation

                    st.markdown("### Export Result")
                    col1, col2, col3 = st.columns(3)
                    export_formats = st.session_state.get('export_formats', ['CSV', 'JSON', 'TXT'])

                    if 'CSV' in export_formats:
                        with col1:
                            data, filename, mime = export_result(result, "CSV", "Inverse_Matrix")
                            st.download_button("📥 Export CSV", data, filename, mime)

                    if 'JSON' in export_formats:
                        with col2:
                            data, filename, mime = export_result(result, "JSON", "Inverse_Matrix")
                            st.download_button("📥 Export JSON", data, filename, mime)

                    if 'TXT' in export_formats:
                        with col3:
                            data, filename, mime = export_result(result, "TXT", "Inverse_Matrix")
                            st.download_button("📥 Export TXT", data, filename, mime)

    elif operation == "Transpose":
        st.subheader("Matrix to Transpose")
        matrix_input = st.text_area(
            "Enter matrix (separate rows with newline, values with spaces):",
            "1 2 3\n4 5 6",
            height=150,
            key="matrix_transpose"
        )

        if st.button("Calculate Transpose", type="primary"):
            a = text_to_numpy(matrix_input)

            if isinstance(a, str):
                st.error("Invalid matrix format")
            else:
                result = transpose(a)
                st.success("Transpose calculated successfully!")
                st.subheader("Result:")
                decimals = st.session_state.get('decimal_places', 2)
                st.code(numpy_to_text(result, decimals=decimals))

                st.session_state['last_result'] = result
                st.session_state['last_operation'] = operation

                st.markdown("### Export Result")
                col1, col2, col3 = st.columns(3)
                export_formats = st.session_state.get('export_formats', ['CSV', 'JSON', 'TXT'])

                if 'CSV' in export_formats:
                    with col1:
                        data, filename, mime = export_result(result, "CSV", "Transpose")
                        st.download_button("📥 Export CSV", data, filename, mime)

                if 'JSON' in export_formats:
                    with col2:
                        data, filename, mime = export_result(result, "JSON", "Transpose")
                        st.download_button("📥 Export JSON", data, filename, mime)

                if 'TXT' in export_formats:
                    with col3:
                        data, filename, mime = export_result(result, "TXT", "Transpose")
                        st.download_button("📥 Export TXT", data, filename, mime)

    elif operation == "Determinant":
        st.subheader("Matrix for Determinant")
        matrix_input = st.text_area(
            "Enter square matrix (separate rows with newline, values with spaces):",
            "4 7\n2 6",
            height=150,
            key="matrix_det"
        )

        if st.button("Calculate Determinant", type="primary"):
            a = text_to_numpy(matrix_input)

            if isinstance(a, str):
                st.error("Invalid matrix format")
            else:
                result = determinant(a)
                if isinstance(result, str):
                    st.error(result)
                else:
                    st.success("Determinant calculated successfully!")
                    st.subheader("Result:")
                    decimals = st.session_state.get('decimal_places', 4)
                    st.metric("det(A)", f"{result:.{decimals}f}")

    elif operation == "Eigenvalues":
        st.subheader("Matrix for Eigenvalues")
        matrix_input = st.text_area(
            "Enter square matrix (separate rows with newline, values with spaces):",
            "4 7\n2 6",
            height=150,
            key="matrix_eigen"
        )

        if st.button("Calculate Eigenvalues", type="primary"):
            a = text_to_numpy(matrix_input)

            if isinstance(a, str):
                st.error("Invalid matrix format")
            else:
                result = eigenvalues(a)
                if isinstance(result, str):
                    st.error(result)
                else:
                    st.success("Eigenvalues calculated successfully!")
                    st.subheader("Result:")
                    decimals = st.session_state.get('decimal_places', 4)
                    for i, val in enumerate(result):
                        if val.imag == 0:
                            st.write(f"λ_{i+1} = {val.real:.{decimals}f}")
                        else:
                            st.write(f"λ_{i+1} = {val.real:.{decimals}f} + {val.imag:.{decimals}f}i")

    elif operation == "Matrix Rank":
        st.subheader("Matrix for Rank")
        matrix_input = st.text_area(
            "Enter matrix (separate rows with newline, values with spaces):",
            "1 2 3\n4 5 6\n7 8 9",
            height=150,
            key="matrix_rank"
        )

        if st.button("Calculate Rank", type="primary"):
            a = text_to_numpy(matrix_input)

            if isinstance(a, str):
                st.error("Invalid matrix format")
            else:
                result = rank(a)
                st.success("Rank calculated successfully!")
                st.subheader("Result:")
                st.metric("rank(A)", result)

    with st.expander("ℹ️ How to use"):
        st.write("""
        **Matrix input format:**
        - Each row on a new line
        - Values separated by spaces or commas
        - Example:
          ```
          1 2 3
          4 5 6
          ```
        
        **Available operations:**
        - **Matrix Multiplication**: A × B (columns in A = rows in B)
        - **Matrix Addition**: A + B (same dimensions required)
        - **Matrix Subtraction**: A - B (same dimensions required)
        - **Inverse Matrix**: A⁻¹ (square matrix, determinant ≠ 0)
        - **Transpose**: Aᵀ (swap rows and columns)
        - **Determinant**: det(A) (square matrix only)
        - **Eigenvalues**: λ (square matrix only)
        - **Matrix Rank**: rank(A) (any matrix)
        """)



