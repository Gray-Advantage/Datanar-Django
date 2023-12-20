const dropZone = document.getElementById("drop_zone");
const deleteFileButton = document.getElementById("deleteFileButton");
const fileInput = document.getElementById("id_links_file");
const longLinklabelNormal = document.getElementById("longLinklabelNormal");
const longLinklabelFile = document.getElementById("longLinklabelFile");
const longLinkField = document.getElementById("id_long_link");
const fileNameField = document.getElementById("fileNameField");
const messageErrorType = document.getElementById("messageErrorType").innerText;
const messageErrorCount = document.getElementById("messageErrorCount").innerText;
const container = document.getElementById("firstContainer");
let timer;

if (fileInput.value === "") {
  longLinkField.value = "";
  longLinkField.readOnly = false;
} else {
  deleteFileButton.classList.remove("d-none");
  longLinklabelFile.classList.remove("d-none");
  longLinklabelNormal.classList.add("d-none");
  longLinkField.readOnly = true;
}

deleteFileButton.addEventListener("click", event => {
  fileInput.value = "";

  deleteFileButton.classList.add("d-none");

  longLinklabelFile.classList.add("d-none");
  longLinklabelNormal.classList.remove("d-none");

  longLinkField.value = "";
  longLinkField.readOnly = false;
  longLinkField.classList.remove("d-none");
  container.insertBefore(longLinkField, container.firstChild);

  fileNameField.value = "";
  fileNameField.classList.add("d-none");
});

dropZone.addEventListener("dragover", event => {
  event.stopPropagation();
  event.preventDefault();

  event.dataTransfer.dropEffect = "copy";
  dropZone.classList.add("blur");
  dropZone.classList.add("cursor-pointer-event-none");

  clearTimeout(timer);
});

dropZone.addEventListener("dragleave", event => {
  event.stopPropagation();
  event.preventDefault();

  clearTimeout(timer);
  timer = setTimeout(() => {
    dropZone.classList.remove("blur");
    dropZone.classList.remove("cursor-pointer-event-none");
  }, 100)
});

dropZone.addEventListener("drop", event => {
  event.stopPropagation();
  event.preventDefault();

  dropZone.classList.remove("blur");
  dropZone.classList.remove("cursor-pointer-event-none");

  const files = event.dataTransfer.files;

  if (files.length > 1) {
    alert(messageErrorCount);
    return;
  }

  const file = files[0];
  const fileName = file.name;
  const fileExtension = fileName.split('.').pop().toLowerCase();
  if (fileExtension !== 'xlsx' && fileExtension !== 'txt') {
    alert(messageErrorType);
    return;
  }

  const reader = new FileReader();
  reader.onload = event => {
    fileInput.files = files;

    deleteFileButton.classList.remove("d-none");

    longLinklabelFile.classList.remove("d-none");
    longLinklabelNormal.classList.add("d-none");

    fileNameField.value = fileName;
    fileNameField.classList.remove("d-none");
    container.insertBefore(fileNameField, container.firstChild);

    longLinkField.value = "https://some.plug.domin.com";
    longLinkField.readOnly = true;
    longLinkField.classList.add("d-none");
  }
  reader.readAsDataURL(file);
});

document.getElementById('mainForm').addEventListener('submit', function() {
  if (fileInput.value) {
    document.getElementById('id_long_link').value = 'https://example.domin.com';
  }
});