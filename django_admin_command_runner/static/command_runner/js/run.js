document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("run-command-form");
  const outputBox = document.getElementById("command-output");
  const spinner = document.getElementById("spinner");

  if (!form || !outputBox || !spinner) {
    console.warn("run_command.js: One or more DOM elements not found.");
    return;
  }

  form.addEventListener("submit", async function (event) {
    event.preventDefault();
    spinner.style.display = "inline-block";
    outputBox.innerText = "";

    const formData = new FormData(form);
    try {
      const response = await fetch(form.action, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      spinner.style.display = "none";

      if (data.success) {
        outputBox.innerText = data.output;
      } else {
        outputBox.innerText = "❌ Error: " + data.error;
      }
    } catch (error) {
      spinner.style.display = "none";
      outputBox.innerText = "❌ Unexpected error: " + error.message;
    }
  });
});
