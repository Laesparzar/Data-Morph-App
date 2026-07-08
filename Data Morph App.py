import os
import threading
import customtkinter as ctk
from tkinter import filedialog, messagebox

try:
    from pypdf import PdfWriter, PdfReader
except ImportError:
    from PyPDF2 import PdfWriter, PdfReader

from PIL import Image


ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")


class PDFConverterMergerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("PDF Converter & Merger")
        self.geometry("950x650")
        self.minsize(850, 580)

        self.pdf_files = []
        self.image_files = []

        self.create_ui()

    def create_ui(self):
        # Main container
        self.main_frame = ctk.CTkFrame(self, corner_radius=15)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="PDF Converter & Merger",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(pady=(20, 5))

        self.subtitle_label = ctk.CTkLabel(
            self.main_frame,
            text="En caso de cualquier problema, conctactar al equipo de Mejora Continua",
            font=ctk.CTkFont(size=12)
        )
        self.subtitle_label.pack(pady=(0, 15))

        # Tabs
        self.tabview = ctk.CTkTabview(self.main_frame, width=880, height=470)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=10)

        self.tab_merge = self.tabview.add("Juntar PDFs")
        self.tab_convert = self.tabview.add("Convertir Imágenes")

        self.create_merge_tab()
        self.create_convert_tab()

        # Progress
        self.progress_label = ctk.CTkLabel(
            self.main_frame,
            text="Listo",
            font=ctk.CTkFont(size=13)
        )
        self.progress_label.pack(pady=(5, 3))

        self.progress_bar = ctk.CTkProgressBar(self.main_frame)
        self.progress_bar.pack(fill="x", padx=30, pady=(0, 15))
        self.progress_bar.set(0)

    # =========================
    # TAB 1 - MERGE PDFS
    # =========================
    def create_merge_tab(self):
        left_frame = ctk.CTkFrame(self.tab_merge, corner_radius=12)
        left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        right_frame = ctk.CTkFrame(self.tab_merge, width=230, corner_radius=12)
        right_frame.pack(side="right", fill="y", padx=10, pady=10)

        self.pdf_listbox = ctk.CTkTextbox(left_frame, wrap="none")
        self.pdf_listbox.pack(fill="both", expand=True, padx=15, pady=15)

        self.pdf_counter_label = ctk.CTkLabel(
            left_frame,
            text="PDFs cargados: 0",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.pdf_counter_label.pack(pady=(0, 10))

        btn_add_files = ctk.CTkButton(
            right_frame,
            text="Agregar PDFs",
            command=self.add_pdf_files,
            height=38
        )
        btn_add_files.pack(fill="x", padx=15, pady=(20, 8))

        btn_add_folder = ctk.CTkButton(
            right_frame,
            text="Agregar Carpeta",
            command=self.add_pdf_folder,
            height=38
        )
        btn_add_folder.pack(fill="x", padx=15, pady=8)

        btn_remove = ctk.CTkButton(
            right_frame,
            text="Quitar Seleccionado",
            command=self.remove_selected_pdf,
            height=38
        )
        btn_remove.pack(fill="x", padx=15, pady=8)

        btn_move_up = ctk.CTkButton(
            right_frame,
            text="Mover Arriba",
            command=self.move_pdf_up,
            height=38
        )
        btn_move_up.pack(fill="x", padx=15, pady=8)

        btn_move_down = ctk.CTkButton(
            right_frame,
            text="Mover Abajo",
            command=self.move_pdf_down,
            height=38
        )
        btn_move_down.pack(fill="x", padx=15, pady=8)

        btn_clear = ctk.CTkButton(
            right_frame,
            text="Limpiar Lista",
            command=self.clear_pdf_list,
            height=38,
            fg_color="#8a1f1f",
            hover_color="#6f1919"
        )
        btn_clear.pack(fill="x", padx=15, pady=8)

        btn_merge = ctk.CTkButton(
            right_frame,
            text="Juntar PDFs",
            command=self.start_merge_pdfs,
            height=45,
            font=ctk.CTkFont(size=15, weight="bold")
        )
        btn_merge.pack(fill="x", padx=15, pady=(35, 15))

    # =========================
    # TAB 2 - CONVERT IMAGES
    # =========================
    def create_convert_tab(self):
        left_frame = ctk.CTkFrame(self.tab_convert, corner_radius=12)
        left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        right_frame = ctk.CTkFrame(self.tab_convert, width=230, corner_radius=12)
        right_frame.pack(side="right", fill="y", padx=10, pady=10)

        self.image_listbox = ctk.CTkTextbox(left_frame, wrap="none")
        self.image_listbox.pack(fill="both", expand=True, padx=15, pady=15)

        self.image_counter_label = ctk.CTkLabel(
            left_frame,
            text="Imágenes cargadas: 0",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.image_counter_label.pack(pady=(0, 10))

        btn_add_images = ctk.CTkButton(
            right_frame,
            text="Agregar Imágenes",
            command=self.add_image_files,
            height=38
        )
        btn_add_images.pack(fill="x", padx=15, pady=(20, 8))

        btn_add_image_folder = ctk.CTkButton(
            right_frame,
            text="Agregar Carpeta",
            command=self.add_image_folder,
            height=38
        )
        btn_add_image_folder.pack(fill="x", padx=15, pady=8)

        btn_clear_images = ctk.CTkButton(
            right_frame,
            text="Limpiar Lista",
            command=self.clear_image_list,
            height=38,
            fg_color="#8a1f1f",
            hover_color="#6f1919"
        )
        btn_clear_images.pack(fill="x", padx=15, pady=8)

        btn_convert_single = ctk.CTkButton(
            right_frame,
            text="Convertir a PDFs Separados",
            command=self.start_convert_images_separate,
            height=42
        )
        btn_convert_single.pack(fill="x", padx=15, pady=(35, 8))

        btn_convert_merged = ctk.CTkButton(
            right_frame,
            text="Unir Imágenes en PDF",
            command=self.start_convert_images_to_single_pdf,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        btn_convert_merged.pack(fill="x", padx=15, pady=8)

    # =========================
    # PDF FUNCTIONS
    # =========================
    def add_pdf_files(self):
        files = filedialog.askopenfilenames(
            title="Selecciona archivos PDF",
            filetypes=[("PDF files", "*.pdf")]
        )

        if files:
            for file in files:
                if file not in self.pdf_files:
                    self.pdf_files.append(file)

            self.refresh_pdf_list()

    def add_pdf_folder(self):
        folder = filedialog.askdirectory(title="Selecciona una carpeta con PDFs")

        if folder:
            pdfs = [
                os.path.join(folder, f)
                for f in os.listdir(folder)
                if f.lower().endswith(".pdf")
            ]

            pdfs.sort()

            for file in pdfs:
                if file not in self.pdf_files:
                    self.pdf_files.append(file)

            self.refresh_pdf_list()

    def refresh_pdf_list(self):
        self.pdf_listbox.delete("1.0", "end")

        for index, file in enumerate(self.pdf_files, start=1):
            self.pdf_listbox.insert(
                "end",
                f"📄 {index}. {os.path.basename(file)}\n"
            )

        self.pdf_counter_label.configure(
            text=f"PDFs cargados: {len(self.pdf_files)}"
        )

    def get_selected_pdf_index(self):
        try:
            selected_text = self.pdf_listbox.get("sel.first", "sel.last")
            first_line = selected_text.splitlines()[0]
            index = int(first_line.split(".")[0]) - 1
            return index
        except Exception:
            messagebox.showwarning(
                "Selección requerida",
                "Selecciona una línea completa o parte del nombre del archivo."
            )
            return None

    def remove_selected_pdf(self):
        index = self.get_selected_pdf_index()

        if index is not None and 0 <= index < len(self.pdf_files):
            self.pdf_files.pop(index)
            self.refresh_pdf_list()

    def move_pdf_up(self):
        index = self.get_selected_pdf_index()

        if index is not None and index > 0:
            self.pdf_files[index], self.pdf_files[index - 1] = (
                self.pdf_files[index - 1],
                self.pdf_files[index],
            )
            self.refresh_pdf_list()

    def move_pdf_down(self):
        index = self.get_selected_pdf_index()

        if index is not None and index < len(self.pdf_files) - 1:
            self.pdf_files[index], self.pdf_files[index + 1] = (
                self.pdf_files[index + 1],
                self.pdf_files[index],
            )
            self.refresh_pdf_list()

    def clear_pdf_list(self):
        self.pdf_files.clear()
        self.refresh_pdf_list()

    def start_merge_pdfs(self):
        if not self.pdf_files:
            messagebox.showwarning("Sin archivos", "Primero agrega archivos PDF.")
            return

        output_file = filedialog.asksaveasfilename(
            title="Guardar PDF final",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")]
        )

        if not output_file:
            return

        thread = threading.Thread(
            target=self.merge_pdfs,
            args=(output_file,),
            daemon=True
        )
        thread.start()

    def merge_pdfs(self, output_file):
        try:
            self.set_progress(0, "Iniciando unión de PDFs...")

            writer = PdfWriter()
            total_files = len(self.pdf_files)

            for i, pdf_path in enumerate(self.pdf_files, start=1):
                try:
                    reader = PdfReader(pdf_path)

                    if reader.is_encrypted:
                        try:
                            reader.decrypt("")
                        except Exception:
                            raise Exception("El PDF está protegido con contraseña.")

                    for page in reader.pages:
                        writer.add_page(page)

                except Exception as e:
                    messagebox.showerror(
                        "Error en PDF",
                        f"No se pudo procesar:\n{pdf_path}\n\nDetalle:\n{e}"
                    )
                    return

                progress = i / total_files
                self.set_progress(
                    progress,
                    f"Procesando PDF {i} de {total_files}..."
                )

            with open(output_file, "wb") as final_pdf:
                writer.write(final_pdf)

            writer.close()

            self.set_progress(1, "PDF final creado correctamente.")

            messagebox.showinfo(
                "Proceso completado",
                f"Se juntaron {total_files} PDFs correctamente:\n\n{output_file}"
            )

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Ocurrió un error al juntar los PDFs:\n\n{e}"
            )
            self.set_progress(0, "Error en el proceso.")

    # =========================
    # IMAGE FUNCTIONS
    # =========================
    def add_image_files(self):
        files = filedialog.askopenfilenames(
            title="Selecciona imágenes",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff *.tif")
            ]
        )

        if files:
            for file in files:
                if file not in self.image_files:
                    self.image_files.append(file)

            self.refresh_image_list()

    def add_image_folder(self):
        folder = filedialog.askdirectory(title="Selecciona una carpeta con imágenes")

        if folder:
            valid_extensions = (".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".tif")

            images = [
                os.path.join(folder, f)
                for f in os.listdir(folder)
                if f.lower().endswith(valid_extensions)
            ]

            images.sort()

            for file in images:
                if file not in self.image_files:
                    self.image_files.append(file)

            self.refresh_image_list()

    def refresh_image_list(self):
        self.image_listbox.delete("1.0", "end")

        for index, file in enumerate(self.image_files, start=1):
            self.image_listbox.insert(
                "end",
                f"{index}. {os.path.basename(file)}\n"
            )

        self.image_counter_label.configure(
            text=f"Imágenes cargadas: {len(self.image_files)}"
        )

    def clear_image_list(self):
        self.image_files.clear()
        self.refresh_image_list()

    def start_convert_images_separate(self):
        if not self.image_files:
            messagebox.showwarning("Sin imágenes", "Primero agrega imágenes.")
            return

        output_folder = filedialog.askdirectory(
            title="Selecciona carpeta de salida"
        )

        if not output_folder:
            return

        thread = threading.Thread(
            target=self.convert_images_separate,
            args=(output_folder,),
            daemon=True
        )
        thread.start()

    def convert_images_separate(self, output_folder):
        try:
            total = len(self.image_files)

            for i, image_path in enumerate(self.image_files, start=1):
                image = Image.open(image_path).convert("RGB")

                file_name = os.path.splitext(os.path.basename(image_path))[0]
                output_pdf = os.path.join(output_folder, f"{file_name}.pdf")

                image.save(output_pdf, "PDF", resolution=100.0)

                self.set_progress(
                    i / total,
                    f"Convirtiendo imagen {i} de {total}..."
                )

            messagebox.showinfo(
                "Proceso completado",
                f"Se convirtieron {total} imágenes a PDF."
            )

            self.set_progress(1, "Imágenes convertidas correctamente.")

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Ocurrió un error al convertir imágenes:\n\n{e}"
            )
            self.set_progress(0, "Error en el proceso.")

    def start_convert_images_to_single_pdf(self):
        if not self.image_files:
            messagebox.showwarning("Sin imágenes", "Primero agrega imágenes.")
            return

        output_file = filedialog.asksaveasfilename(
            title="Guardar PDF final",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")]
        )

        if not output_file:
            return

        thread = threading.Thread(
            target=self.convert_images_to_single_pdf,
            args=(output_file,),
            daemon=True
        )
        thread.start()

    def convert_images_to_single_pdf(self, output_file):
        try:
            images = []
            total = len(self.image_files)

            for i, image_path in enumerate(self.image_files, start=1):
                img = Image.open(image_path).convert("RGB")
                images.append(img)

                self.set_progress(
                    i / total,
                    f"Cargando imagen {i} de {total}..."
                )

            first_image = images[0]
            remaining_images = images[1:]

            first_image.save(
                output_file,
                save_all=True,
                append_images=remaining_images,
                resolution=100.0
            )

            for img in images:
                img.close()

            self.set_progress(1, "PDF de imágenes creado correctamente.")

            messagebox.showinfo(
                "Proceso completado",
                f"Se creó el PDF correctamente:\n\n{output_file}"
            )

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Ocurrió un error al unir imágenes en PDF:\n\n{e}"
            )
            self.set_progress(0, "Error en el proceso.")

    # =========================
    # UTILS
    # =========================
    def set_progress(self, value, text):
        self.progress_bar.set(value)
        self.progress_label.configure(text=text)
        self.update_idletasks()


if __name__ == "__main__":
    app = PDFConverterMergerApp()
    app.mainloop()