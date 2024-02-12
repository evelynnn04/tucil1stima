import flet as ft
import shutil
from flet import *
import function as func

def main(page: ft.Page):
    matrix = []
    sequences = []
    sequences_score = []

    def build_matrix(width, height):
        matrix.clear()
        for _ in range(height):
            row = []
            for _ in range(width):
                field = ft.TextField(text_align="center", width=50)
                row.append(field)
            matrix.append(row)
        page.update()

    def build_sequences(width, height):
        sequences.clear()
        for _ in range(height):
            row = []
            for _ in range(width):
                field = ft.TextField(text_align="center", width=50)
                row.append(field)
            sequences.append(row)
        page.update()

    def build_sequences_score(height):
        sequences_score.clear()
        for _ in range(height):
            row = []
            for _ in range(1):
                field = ft.TextField(text_align="center", width=50)
                row.append(field)
            sequences_score.append(row)
        page.update()

    def update_size(e):
        matrixWidth = int(width_input.value)
        matrixHeight = int(height_input.value)
        sequencesWidth = int(sequences_width_input.value)
        sequencesHeight = int(sequences_height_input.value)
        build_matrix(matrixWidth, matrixHeight)
        build_sequences(sequencesWidth, sequencesHeight)
        build_sequences_score(sequencesHeight)
        page.controls.remove(matrix_view)
        page.update()
        buffer_input = ft.Row([buffer_size_input], alignment=ft.MainAxisAlignment.CENTER, disabled=True)
        new_matrix_view = ft.Row(
            [
                ft.Column(
                    [
                        ft.Row([width_input, height_input], alignment=ft.MainAxisAlignment.CENTER, disabled=True),
                        ft.Container(height=2),
                        ft.Container(height=10),
                        *[ft.Row(row, alignment=ft.MainAxisAlignment.CENTER) for row in matrix]
                    ]
                ),
                ft.Container(width=50),  
                ft.Column(
                    [
                        ft.Row([sequences_width_input, sequences_height_input], alignment=ft.MainAxisAlignment.CENTER, disabled=True),
                        ft.Container(height=2),
                        ft.Container(height=10),
                        *[ft.Row(row, alignment=ft.MainAxisAlignment.CENTER) for row in sequences]
                    ]
                ),
                ft.Container(width=20),
                ft.Column(
                    [
                        ft.Container(height=50),
                        ft.Text(value="Score", size=19),
                        *[ft.Row(row, alignment=ft.MainAxisAlignment.CENTER) for row in sequences_score]
                    ]
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
        solver = ft.Row(
            [
                ft.Row([solve_button], alignment=ft.MainAxisAlignment.CENTER)
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
        page.controls.append(buffer_input)
        page.controls.append(ft.Container(height=20))
        page.controls.append(new_matrix_view)
        page.controls.append(ft.Container(height=20))
        page.controls.append(solver)
        page.update()

    def solve(e):
        matrixWidth = int(width_input.value)
        matrixHeight = int(height_input.value)
        bufferSize = int(buffer_size_input.value)
        matrix_value = []
        for row in matrix:
            row_value = []
            for field in row:
                row_value.append(field.value)
            matrix_value.append(row_value)
        sequence_value = []
        for row in sequences:
            row_value = []
            for field in row:
                row_value.append(field.value)
            sequence_value.append(row_value)
        sequences_score_value = [] 
        for row in sequences_score:
            for field in row:
                sequences_score_value.append(int(field.value))
        result, score, coordinate = func.solver(matrixWidth, matrixHeight, bufferSize, sequence_value
        , sequences_score_value, matrix_value)
        print(sequences_score_value)
        print(result, score, coordinate)
        with open("result.txt", 'w') as outputFile:
            outputFile.write(str(score) + '\n')
            outputFile.write(' '.join(map(str, result)) + '\n')
            outputFile.write('\n'.join(map(str, coordinate)) + '\n')
        result_output = ft.Text(value=f"Optimal Buffer: {', '.join(result)}", size=17)
        score_output = ft.Text(value=f"Optimal Score: {score}", size=17)
        coordinate_output = ft.Text(value=f"Coordinate: {', '.join(coordinate)}", size=17)
        success_message = ft.Text(value="Succed to save!")
        result_row = ft.Row(
            [
                ft.Column(
                    [
                        ft.Row([result_output], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Container(height=10),
                        ft.Row([score_output], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Container(height=10),
                        ft.Row([coordinate_output], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Container(height=10),
                        ft.Row([success_message], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Container(height=10),
                    ]
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
        page.controls.append(ft.Container(height=20))
        page.controls.append(result_row)
        page.update()

    def solve_from_txt(e):
        with open(str(upload_file_input.value), 'r') as inputFile:
                bufferSize = int(inputFile.readline())
                matrixWidth, matrixHeight = map(int, inputFile.readline().split())
                matrix = [inputFile.readline().split() for _ in range(matrixHeight)]
                numberOfSequences = int(inputFile.readline())
                line_number = 0
                sequence = []
                sequenceReward = []
                for line in inputFile:
                    if line_number % 2 == 0:
                        sequence.append(line.split())
                    else:
                        sequenceReward.append(line.strip())
                    line_number += 1
        result, score, coordinate = func.solver(matrixWidth, matrixHeight, bufferSize, sequence, sequenceReward, matrix)
        with open("result.txt", 'w') as outputFile:
            outputFile.write(str(score) + '\n')
            outputFile.write(' '.join(map(str, result)) + '\n')
            outputFile.write('\n'.join(map(str, coordinate)) + '\n')
        file_input_name = ft.Text(value=f"File Input: {(upload_file_input.value)}", size=17)
        result_output = ft.Text(value=f"Optimal Buffer: {', '.join(result)}", size=17)
        score_output = ft.Text(value=f"Optimal Score: {score}", size=17)
        coordinate_output = ft.Text(value=f"Coordinate: {', '.join(coordinate)}", size=17)
        success_message = ft.Text(value="Succed to save!")
        result_row = ft.Row(
            [
                ft.Column(
                    [
                        ft.Row([file_input_name], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Row([result_output], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Row([score_output], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Row([coordinate_output], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Row([success_message], alignment=ft.MainAxisAlignment.CENTER),
                    ]
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
        page.controls.append(ft.Container(height=20))
        page.controls.append(result_row)
        page.update()

    #Button, text, and field
    title = ft.Text(value="Cyberpunk 2077 Breach Protocol", size=50)
    width_input = ft.TextField(label="Matrix Width", width=130)
    height_input = ft.TextField(label="Matrix Height", width=130)
    buffer_size_input = ft.TextField(label="Buffer size", width=130)
    fix_size = ft.FilledButton(text="Fix Size", on_click=update_size, height=35)
    sequences_width_input = ft.TextField(label="Sequences Max", width=170)
    sequences_height_input = ft.TextField(label="Number of Sequences", width=170)
    solve_button = ft.FilledButton(text="SOLVE AND SAVE", on_click=solve)
    upload_file_input = ft.TextField(label="or input file name here...", width=300)
    upload_file_button = ft.FilledButton(text="SOLVE AND SAVE", on_click=solve_from_txt, height=35)
    
    matrix_view = ft.Row(
            [
                ft.Column(
                    [
                        ft.Row([width_input, height_input, sequences_width_input, sequences_height_input, buffer_size_input], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Container(height=7),
                        ft.Row([fix_size], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Container(height=7),
                        ft.Row([upload_file_input, upload_file_button], alignment=ft.MainAxisAlignment.CENTER),
                    ]
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

    page.add(
        ft.Container(height=7),
        ft.Row([title], alignment=ft.MainAxisAlignment.CENTER),
        ft.Container(height=7)
    )
    page.controls.append(matrix_view)
    page.add(
        ft.Container(height=2),
    )
    page.scroll = "always"

ft.app(target=main)
