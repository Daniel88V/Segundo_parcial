import tkinter as tk
from tkinter import messagebox
class Candidatas:
    def __init__(self, codigo, nombre, edad, institucion, municipio):
        self.codigo = codigo
        self.nombre = nombre
        self.edad = edad
        self.institucion = institucion
        self.municipio = municipio
    def mostrar_candidata(self):
        return f"Codigo: {self.codigo} | Nombre: {self.nombre} | Edad: {self.edad} | Institucion: {self.institucion} | Municipio: {self.municipio}"
class Jurados:
    def __init__(self, nombre, especialidad = "General"):
        self.nombre = nombre
        self.especialidad = especialidad
    def mostrar_jurado(self):
        return f"Jurado: {self.nombre}"
class Calificaciones:
    def __init__(self, cultura_g, proyeccion_e, entrevista):
        self.cultura_g = cultura_g
        self.proyeccion_e = proyeccion_e
        self.entrevista = entrevista
    @property
    def promedio(self):
        return (self.cultura_g + self.proyeccion_e + self.entrevista) / 3
class Participantes(Candidatas):
    def __init__(self, codigo, nombre, edad, institucion, municipio):
        super().__init__(codigo, nombre, edad, institucion, municipio)
        self._puntajes = {}
        self.jurados_total = {}
    def registrar_puntajes(self, puntajes):
        criterios = ["Cultura_G", "Proyección_E", "Entrevista"]
        if not all(criterio in puntajes for criterio in criterios):
            raise ValueError("Faltan criterios por llenar")
        for criterio, puntaje in puntajes.items():
            if not isinstance(puntaje, (int, float)) or not (0 <= puntaje <= 10):
                raise ValueError(f"Error. El puntaje para {criterio} debe de ser entre 0 y 10.")
            self._puntajes[criterio] = puntaje
    @property
    def total(self):
        return (sum(self._puntajes.values()))/3 if self._puntajes else 0
    def mostrar_puntajes(self):
        info = super().mostrar_candidata()
        if self._puntajes:
            info += f"Puntaje total: {self.total}"
            info += f"Puntaje por criterio: {self._puntajes}"
        else:
            info += "No se ha registrado un puntaje"
        return info
class Concurso:
    def __init__(self):
        self._participantes = []
        self._jurados = []
    def inscribir_participantes(self, participante):
        for p in self._participantes:
            if p.codigo.lower() == participante.codigo.lower():
                return False
        self._participantes.append(participante)
        return True
    def anadir_jurado(self, jurado):
        self._jurados.append(jurado)
        return True
    def calificacion(self, nombre, puntaje):
        participante = self._buscar_participante(nombre)
        if participante:
            participante.registrar_puntajes(puntaje)
            return True
        return False
    def _buscar_participante(self, nombre):
        for n in self._participantes:
            if n.codigo.lower() == nombre.lower():
                return n
        return None
    def conseguir_participante(self):
        return self._participantes
    def ranking(self):
        evaluacion = [p for p in self._participantes if p.total > 0]
        ranking_final =  sorted(
            evaluacion,
            key=lambda p: (p.total, p._puntajes.get("Cultura_G", 0)),
            reverse=True
        )
        return ranking_final
class ConcursoApp:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Reina de Independecia 2025")
        self.ventana.geometry("700x500")
        self.concurso = Concurso()
        self.menu()
        tk.Label(
            self.ventana,
            text="Sistema de inscripción y evaluación de candidatas a reinas 2025",
            font=("Arial", 12, "bold"),
            justify = "center"
        ).pack(pady = 50)
        self.ventana.mainloop()
    def menu(self):
        barra = tk.Menu(self.ventana)
        opciones = tk.Menu(barra, tearoff = 0)
        opciones.add_command(label = "Inscribir señorita", command = self.inscribir_participante)
        opciones.add_command(label="Añadir jurado", command=self.anadir_jurado)
        opciones.add_command(label="Calificar", command=self.calificar)
        #opciones.add_command(label="Mostrar ranking", command=self.mostrar_ranking)
        opciones.add_separator()
        opciones.add_command(label="Salir", command=self.ventana.quit)
        barra.add_cascade(label="Opciones", menu=opciones)
        self.ventana.config(menu = barra)
    def inscribir_participante(self):
        ventana_inscripcion = tk.Toplevel(self.ventana)
        ventana_inscripcion.title("Inscribir señorita")
        ventana_inscripcion.geometry("400x250")
        tk.Label(ventana_inscripcion, text = "Código de participante: ").pack(pady = 5)
        codigo_entry = tk.Entry(ventana_inscripcion)
        codigo_entry.pack(pady = 5)
        tk.Label(ventana_inscripcion, text="Nombre de la participante: ").pack(pady=5)
        nombre_entry = tk.Entry(ventana_inscripcion)
        nombre_entry.pack(pady=5)
        tk.Label(ventana_inscripcion, text="Edad de la participante: ").pack(pady=5)
        edad_entry = tk.Entry(ventana_inscripcion)
        edad_entry.pack(pady=5)
        tk.Label(ventana_inscripcion, text="Institución de participante: ").pack(pady=5)
        institucion_entry = tk.Entry(ventana_inscripcion)
        institucion_entry.pack(pady=5)
        tk.Label(ventana_inscripcion, text="Municipio de participante: ").pack(pady=5)
        municipio_entry = tk.Entry(ventana_inscripcion)
        municipio_entry.pack(pady=5)
        def guardar():
            codigo = codigo_entry.get()
            nombre = nombre_entry.get()
            edad = edad_entry.get()
            institucion = institucion_entry.get()
            municipio = municipio_entry.get()
            if not codigo or not nombre or not edad or not institucion or not municipio:
                messagebox.showwarning("Error", "Todos los campos deben de ser completados")
                return
            try:
                nueva_participante = Participantes(codigo, nombre, edad, institucion, municipio)
                if self.concurso.inscribir_participantes(nueva_participante):
                    messagebox.showinfo("Exito", "La participante se ha agregado correctamente")
                    ventana_inscripcion.destroy()
                else:
                    messagebox.showwarning("Error", "Ya existe una participante con ese código")
            except ValueError as e:
                messagebox.showerror("Error de Validación", str(e))
        tk.Button(ventana_inscripcion, text = "Guardar", command = guardar).pack(pady = 10)
    def anadir_jurado(self):
        ventana_inscripcion = tk.Toplevel(self.ventana)
        ventana_inscripcion.title("Añadir jurado")
        ventana_inscripcion.geometry("400x250")
        tk.Label(ventana_inscripcion, text="Nombre del jurado: ").pack(pady=5)
        nombre_entry = tk.Entry(ventana_inscripcion)
        nombre_entry.pack(pady=5)
        def guardar_jurado():
            nombre = nombre_entry.get()
            if not nombre:
                messagebox.showwarning("Error. Debe de ingresar el nombre")
                return
            try:
                nuevo_jurado = Jurados(nombre)
                if self.concurso.anadir_jurado(nuevo_jurado):
                    messagebox.showinfo("Exito", "Jurado se ha agregado correctamente")
                    ventana_inscripcion.destroy()
            except ValueError as e:
                messagebox.showerror("Error de Validación", str(e))
        tk.Button(ventana_inscripcion, text = "Guardar", command = guardar_jurado).pack(pady = 5)
    def calificar(self):
        ventana_calificacion = tk.Toplevel(self.ventana)
        ventana_calificacion.title("Calificar participante")
        ventana_calificacion.geometry("400x250")
        participantes_inscritas = self.concurso.conseguir_participante()
        if not participantes_inscritas:
            messagebox.showinfo("Info", "No hay señoritas inscritas")
            ventana_calificacion.destroy()
            return
        tk.Label(ventana_calificacion, text = "Seleccione a la participante: ").pack(pady=5)
        participante_var = tk.StringVar(ventana_calificacion)
        participante_var.set(participantes_inscritas[0].nombre)
        participante_menu = tk.OptionMenu(ventana_calificacion, participante_var, *[p.nombre for p in participantes_inscritas])
        participante_menu.pack(pady = 5)
        criterios = ["Cultura_G", "Proyección_E", "Entrevista"]
        entry_widget = {}
        for criterio in criterios:
            tk.Label(ventana_calificacion, text = f"Puntaje de {criterio} (0-10").pack(pady = 2)
            entry = tk.Entry(ventana_calificacion)
            entry.pack(pady = 2)
            entry_widget[criterio] = entry
        def guardar_calificar():
            participante_seleccionada = participante_var.get()
            puntajes = {}
            try:
                for criterio, entry in entry_widget.items():
                    puntaje = float(entry.get())
                    puntajes[criterio] = puntaje
                if self.concurso.calificacion(participante_seleccionada, puntajes):
                    messagebox.showinfo("Exito", "Calificacion guardada correctamente")
                    ventana_calificacion.destroy()
                else:
                    messagebox.showwarning("Info", "No se encuentra a la participante")
            except ValueError as e:
                messagebox.showerror("Error", "Todos los puntajes deben de ser números validos")
        tk.Button(ventana_calificacion, text = "Guardar", command = guardar_calificar).pack(pady = 10)

if __name__ == "__main__":
    ConcursoApp()