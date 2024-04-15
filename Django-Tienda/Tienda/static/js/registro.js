
const formulario = document.querySelector("#registro");

document.querySelector('#limpiar').addEventListener('click', (e) => {
  formulario.reset();
})

/*
formulario.addEventListener("submit", (e) => {
  e.preventDefault();
  revisarFormulario();
});

function revisarFormulario() {
  const formData = new FormData(formulario)
  const contraseña1 = formData.get('contraseña')
  const contraseña2 = formData.get('confirmar')
  const nacimiento = formData.get('nacimiento')
  const fechaNacimiento = new Date(nacimiento);
  const fechaActual = new Date();

  let edad = fechaActual - fechaNacimiento
  edad = edad / 1000
  edad = edad / 60
  edad = edad / 60
  edad = edad / 24
  edad = edad / 365

  if(edad < 13) {
    alert('Los menores de 13 años no pueden registarse')
    return
  }

  if(contraseña1 !== contraseña2) {
    alert('Las contraseñas deben coincidir')
    return
  }

  if(contraseña1.length < 6 || contraseña1.length > 18) {
    alert('La contraseña debe tener entre 6 y 18 carácteres')
    return
  }

  if(contraseña1.search(/[A-Z]/) < 0) {
    alert('La contraseña necesita al menos una mayúscula')
    return
  }

  if(contraseña1.search(/[0-9]/) < 0) {
    alert('Tu contraseña necesita al menos un número')
    return
  }

  formData.submit()
}
*/