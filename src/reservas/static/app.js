"use strict";

const $ = (selector) => document.querySelector(selector);
const formClientes = $("#form-clientes");
const formServicios = $("#form-servicios");
const formReservas = $("#form-reservas");
const alternativas = $("#alternativas");

function mensaje(texto, error = false) {
  const elemento = $("#mensaje");
  elemento.textContent = texto;
  elemento.classList.toggle("error", error);
}

async function api(url, opciones = {}) {
  let response;

  try {
    response = await fetch(url, {
      cache: "no-store",
      ...opciones,
    });
  } catch {
    throw new Error(
      "No se pudo comunicar con el servidor. " +
      "Si estabas guardando, consulta la lista antes de reintentar."
    );
  }

  let data;
  try {
    data = await response.json();
  } catch {
    throw new Error(
      "El servidor devolvió una respuesta inesperada. " +
      "Consulta la lista antes de repetir la operación."
    );
  }

  if (!response.ok) {
    const error = new Error(data.error || "No se pudo completar la operación.");
    error.status = response.status;
    error.alternativas = data.alternativas || [];
    throw error;
  }

  return data;
}

function enviar(url, metodo, datos) {
  return api(url, {
    method: metodo,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(datos),
  });
}

function bloquearFormulario(form) {
  const controles = [...form.elements];
  const estados = controles.map((control) => control.disabled);

  controles.forEach((control) => {
    control.disabled = true;
  });

  return () => {
    controles.forEach((control, index) => {
      control.disabled = estados[index];
    });
  };
}

function estadoTabla(selector, texto, columnas) {
  const cuerpo = $(selector);
  const fila = document.createElement("tr");
  const celda = document.createElement("td");

  celda.colSpan = columnas;
  celda.textContent = texto;
  fila.append(celda);
  cuerpo.replaceChildren(fila);
}

function celda(fila, valor) {
  const elemento = document.createElement("td");
  elemento.textContent = valor ?? "—";
  fila.append(elemento);
  return elemento;
}

function boton(texto, accion) {
  const elemento = document.createElement("button");
  elemento.type = "button";
  elemento.textContent = texto;
  elemento.addEventListener("click", accion);
  return elemento;
}

function llenarSelector(nombre, elementos, etiqueta) {
  const selector = formReservas.elements.namedItem(nombre);
  const seleccionado = selector.value;
  const vacio = document.createElement("option");

  vacio.value = "";
  vacio.textContent = etiqueta;
  selector.replaceChildren(vacio);

  for (const item of elementos) {
    const opcion = document.createElement("option");
    opcion.value = String(item.id);
    opcion.textContent = item.nombre;
    selector.append(opcion);
  }

  selector.value = seleccionado;
  if (!selector.value) {
    selector.value = "";
  }
}

async function cargarClientes() {
  estadoTabla("#lista-clientes", "Cargando clientes…", 4);

  try {
    const clientes = await api("/api/clientes");
    const cuerpo = $("#lista-clientes");
    cuerpo.replaceChildren();

    for (const cliente of clientes) {
      const fila = document.createElement("tr");
      celda(fila, cliente.nombre);
      celda(fila, cliente.telefono);
      celda(fila, cliente.email);

      celda(fila, "").append(boton("Editar", () => {
        if (formClientes.dataset.ocupado === "true") return;

        for (const campo of ["id", "nombre", "telefono", "email"]) {
          formClientes.elements.namedItem(campo).value =
            cliente[campo] ?? "";
        }

        mensaje(`Editando cliente ${cliente.id}.`);
        formClientes.elements.namedItem("nombre").focus();
      }));

      cuerpo.append(fila);
    }

    if (!clientes.length) {
      estadoTabla("#lista-clientes", "No hay clientes registrados.", 4);
    }

    llenarSelector("cliente_id", clientes, "Selecciona un cliente");
  } catch (error) {
    estadoTabla("#lista-clientes", "No se pudieron cargar los clientes.", 4);
    throw error;
  }
}

async function cargarServicios() {
  estadoTabla("#lista-servicios", "Cargando servicios…", 3);

  try {
    const servicios = await api("/api/servicios");
    const cuerpo = $("#lista-servicios");
    cuerpo.replaceChildren();

    for (const servicio of servicios) {
      const fila = document.createElement("tr");
      celda(fila, servicio.nombre);
      celda(fila, `S/ ${servicio.precio}`);
      celda(fila, `${servicio.duracion_minutos} minutos`);
      cuerpo.append(fila);
    }

    if (!servicios.length) {
      estadoTabla("#lista-servicios", "No hay servicios registrados.", 3);
    }

    llenarSelector("servicio_id", servicios, "Selecciona un servicio");
  } catch (error) {
    estadoTabla("#lista-servicios", "No se pudieron cargar los servicios.", 3);
    throw error;
  }
}

function fechaLima(valor) {
  return new Intl.DateTimeFormat("es-PE", {
    timeZone: "America/Lima",
    dateStyle: "short",
    timeStyle: "short",
    hour12: false,
  }).format(new Date(valor));
}

async function cancelarReserva(reserva, control) {
  const confirmado = window.confirm(
    `¿Cancelar la reserva ${reserva.id} de ${reserva.cliente}?`
  );
  if (!confirmado) return;

  control.disabled = true;
  let guardado = false;

  try {
    await api(`/api/reservas/${reserva.id}/cancelar`, {
      method: "POST",
    });
    guardado = true;
    await cargarReservas();
    mensaje(`Reserva ${reserva.id} cancelada. Su historial se conserva.`);
  } catch (error) {
    mensaje(
      guardado
        ? "La cancelación se guardó, pero no se pudo actualizar la lista."
        : error.message,
      true
    );
  } finally {
    control.disabled = false;
  }
}

async function cargarReservas() {
  estadoTabla("#lista-reservas", "Cargando reservas…", 7);

  try {
    const reservas = await api("/api/reservas");
    const cuerpo = $("#lista-reservas");
    cuerpo.replaceChildren();

    for (const reserva of reservas) {
      const fila = document.createElement("tr");
      celda(fila, reserva.cliente);
      celda(fila, reserva.servicio);
      celda(fila, fechaLima(reserva.inicio));
      celda(fila, fechaLima(reserva.fin));
      celda(fila, `S/ ${reserva.precio_aplicado}`);

      const estado = celda(fila, reserva.estado);
      estado.className = "estado";

      if (reserva.cancelado_en) {
        estado.title = `Cancelada: ${fechaLima(reserva.cancelado_en)}`;
      }

      const acciones = celda(fila, "");

      if (
        reserva.estado === "Confirmada" &&
        new Date(reserva.inicio).getTime() > Date.now()
      ) {
        const control = boton("Cancelar", () => {
          cancelarReserva(reserva, control);
        });
        acciones.append(control);
      } else {
        acciones.textContent =
          reserva.estado === "Cancelada" ? "Cancelación registrada" : "Ya iniciada";
      }

      cuerpo.append(fila);
    }

    if (!reservas.length) {
      estadoTabla("#lista-reservas", "No hay reservas registradas.", 7);
    }
  } catch (error) {
    estadoTabla("#lista-reservas", "No se pudieron cargar las reservas.", 7);
    throw error;
  }
}

function mostrarAlternativas(opciones) {
  alternativas.replaceChildren();
  if (!opciones.length) return;

  const titulo = document.createElement("h3");
  titulo.textContent = "Horarios alternativos disponibles";

  const ayuda = document.createElement("p");
  ayuda.textContent =
    "Selecciona una opción y pulsa Confirmar reserva. " +
    "La disponibilidad se verificará nuevamente.";

  const seleccion = document.createElement("p");
  seleccion.setAttribute("role", "status");

  alternativas.append(titulo, ayuda);

  for (const opcion of opciones) {
    const control = boton(
      `${fechaLima(opcion.inicio)} – ${fechaLima(opcion.fin)}`,
      () => {
        const campo = formReservas.elements.namedItem("inicio");

        // El servidor devuelve estas alternativas en hora de Lima.
        campo.value = opcion.inicio.slice(0, 16);

        if (!campo.value) {
          mensaje("No se pudo seleccionar el horario.", true);
          return;
        }

        alternativas.querySelectorAll("button").forEach((elemento) => {
          elemento.setAttribute("aria-pressed", "false");
        });

        control.setAttribute("aria-pressed", "true");

        seleccion.textContent =
          `Seleccionado: ${fechaLima(opcion.inicio)}. ` +
          "Pulsa Confirmar reserva para registrarlo.";

        mensaje("Horario seleccionado; la reserva aún no está confirmada.");
      }
    );

    control.setAttribute("aria-pressed", "false");
    alternativas.append(control);
  }

  alternativas.append(seleccion);
}

function conectarFormulario(form, preparar, actualizar, textoExito) {
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (form.dataset.ocupado === "true") return;
    if (!form.reportValidity()) return;

    const solicitud = preparar(new FormData(form));
    form.dataset.ocupado = "true";
    const desbloquear = bloquearFormulario(form);
    let guardado = false;

    if (form === formReservas) {
      alternativas.replaceChildren();
    }

    mensaje("Guardando…");

    try {
      await enviar(solicitud.url, solicitud.metodo, solicitud.datos);
      guardado = true;
      form.reset();

      if (form === formClientes) {
        form.elements.namedItem("id").value = "";
      }

      await actualizar();
      mensaje(textoExito);
    } catch (error) {
      if (form === formReservas && error.status === 409) {
        mostrarAlternativas(error.alternativas);
      }

      mensaje(
        guardado
          ? "La operación se guardó, pero no se pudo actualizar la lista."
          : error.message,
        true
      );
    } finally {
      desbloquear();
      form.dataset.ocupado = "false";
    }
  });
}

conectarFormulario(
  formClientes,
  (datos) => {
    const id = datos.get("id");
    return {
      url: id ? `/api/clientes/${id}` : "/api/clientes",
      metodo: id ? "PUT" : "POST",
      datos: {
        nombre: datos.get("nombre"),
        telefono: datos.get("telefono"),
        email: datos.get("email") || null,
      },
    };
  },
  async () => {
    await cargarClientes();
    await cargarReservas();
  },
  "Cliente guardado correctamente."
);

conectarFormulario(
  formServicios,
  (datos) => ({
    url: "/api/servicios",
    metodo: "POST",
    datos: {
      nombre: datos.get("nombre"),
      precio: datos.get("precio"),
      duracion_minutos: Number(datos.get("duracion_minutos")),
    },
  }),
  cargarServicios,
  "Servicio registrado correctamente."
);

conectarFormulario(
  formReservas,
  (datos) => ({
    url: "/api/reservas",
    metodo: "POST",
    datos: {
      cliente_id: Number(datos.get("cliente_id")),
      servicio_id: Number(datos.get("servicio_id")),
      inicio: datos.get("inicio"),
    },
  }),
  cargarReservas,
  "Reserva confirmada correctamente."
);

$("#limpiar-cliente").addEventListener("click", () => {
  formClientes.reset();
  formClientes.elements.namedItem("id").value = "";
  mensaje("Formulario preparado para un nuevo cliente.");
  formClientes.elements.namedItem("nombre").focus();
});

for (const [selector, cargar] of [
  ["#recargar-clientes", cargarClientes],
  ["#recargar-servicios", cargarServicios],
  ["#recargar-reservas", cargarReservas],
]) {
  $(selector).addEventListener("click", async (event) => {
    const control = event.currentTarget;
    control.disabled = true;
    mensaje("Actualizando…");

    try {
      await cargar();
      mensaje("Lista actualizada.");
    } catch (error) {
      mensaje(error.message, true);
    } finally {
      control.disabled = false;
    }
  });
}

async function iniciar() {
  mensaje("Cargando información…");

  const resultados = await Promise.allSettled([
    cargarClientes(),
    cargarServicios(),
    cargarReservas(),
  ]);

  const fallo = resultados.find((item) => item.status === "rejected");
  mensaje(
    fallo ? fallo.reason.message : "Información actualizada.",
    Boolean(fallo)
  );
}

iniciar();