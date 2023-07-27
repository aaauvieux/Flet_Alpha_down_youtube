import os
from pytube import YouTube
import flet as ft 

from ctypes import windll, byref
from ctypes.wintypes import DWORD
from socket import gethostbyname, create_connection, error

from tkinter import filedialog

def pideNombreArchivo(events):
    ruta_archivo = filedialog.asksaveasfilename(defaultextension=".MP4",
                                                filetypes=[("Archivos de Video", "*.MP4"),])
    head, tail = os.path.split(ruta_archivo)
    print(head)
    print(tail)
    print(ruta_archivo)
    return ruta_archivo

def comprobarConexion():
    try:
        gethostbyname("google.com")
        conexion = create_connection(("google.com", 80), 1)
        conexion.close()
        print("si")
        return True
    except error:
        print("no")
        return False


def main(page: ft.Page):
    page.title = "Descarga tu video favorito"
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    def accion(events):
        txt_nombreArchivo = pideNombreArchivo()
        page.update()

        if comprobarConexion:
            page.splash = ft.ProgressBar()
            page.update()
            enlace = txt_video.value
            if enlace == "":
                dlg = ft.AlertDialog(title=ft.Text("Debe ingresar el link del video para descargar;\nComo pretendes descargar sin poner el link????"), on_dismiss=lambda e: print("Sin link"))
                page.dialog = dlg
                dlg.open = True
                page.update()
            else:
                video = YouTube(enlace)
                selection = drp_resolucion.value
                if selection:
                    txt_video.disabled = True
                    drp_resolucion.disabled = True
                    btn_descargar.disabled = True
                    txt_descargando.visible=True
                    page.update()
                    if selection=="Resolución ALTA":
                        descarga = video.streams.get_highest_resolution()
                    if selection=="Resolución BAJA":
                        descarga = video.streams.get_lowest_resolution()
                    if selection=="Solo AUDIO":
                        descarga = video.streams.get_audio_only()
                    descarga.download()
                else:
                    dlg = ft.AlertDialog(title=ft.Text("Debe ingresar la resolución del video para descargar;\nPor favor preste atenci+on!!!"), on_dismiss=lambda e: print("Sin Resolucion"))
                    page.dialog = dlg
                    dlg.open = True
                    page.update()
            txt_video.disabled = False
            drp_resolucion.disabled = False
            btn_descargar.disabled = False
            page.splash = None
            txt_descargando.visible=False
            page.update()
        else:

            dlg = ft.AlertDialog(title=ft.Text("SIN CONEXION A INTERNET!!!"), on_dismiss=lambda e: print("Sin Conexion"))
            page.dialog = dlg
            dlg.open = True
            page.update()
            
    txt_descargando = ft.Text("Descargando...", size=32,color=ft.colors.RED,bgcolor=ft.colors.WHITE,weight=ft.FontWeight.BOLD)
    txt_descargando.visible=False
    txt_video = ft.TextField(hint_text="Ingrese el link del video para descargar",text_align=ft.Text.right, width=500)
    txt_nombreArchivo = ft.TextField(hint_text="Seleccione la ubicación y el nombre de archivo a guardar",text_align=ft.Text.right, width=500)
    txt_nombreArchivo.enabled=False
    btn_descargar = ft.ElevatedButton(text="Descargar", on_click=accion)
    btn_nombreArchivo = ft.ElevatedButton(text="...", on_click=pideNombreArchivo)
    drp_resolucion = ft.Dropdown(
        label="Resolución",
        hint_text="Selecione la Resolución",
        width=200,
        options=[
            ft.dropdown.Option("Resolución ALTA"),
            ft.dropdown.Option("Resolución BAJA"),
            ft.dropdown.Option("Solo AUDIO"),
        ]
    )
    img = ft.Image(
        src=f"./assets/fondo.png",
        width=600,
        height=300,
        border_radius=10,
        fit=ft.ImageFit.FILL)
            
    page.add(
        ft.Container(
            content=ft.Stack([
                        img,
                        ft.Column([
                            txt_video,
                            drp_resolucion,
                            ft.Row([txt_nombreArchivo,btn_nombreArchivo]),
                            btn_descargar,
                            txt_descargando
                    ]),
                    ],
                    width=600,
                    height=300,
                    ),
            margin=0,
            padding=0,
            alignment=ft.alignment.center,
            bgcolor=ft.colors.RED,
            width=600,
            height=300,
            border_radius=10,
        )
    )
    
#Ejecucion en escritorio
ft.app(target=main)

#Ejecucion WEB
#ft.app(target=main, view=ft.AppView.WEB_BROWSER)
