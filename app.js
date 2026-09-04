(() => {
  const MAX_SIZE = 50 * 1024 * 1024;
  const el = (id) => document.getElementById(id);
  const input = el("pdfInput");
  const dropZone = el("dropZone");
  const emptyState = el("emptyState");
  const workspace = el("workspace");
  const errorMessage = el("errorMessage");
  const canvas = el("pdfCanvas");
  const context = canvas.getContext("2d");

  let pdfDocument = null;
  let currentPage = 1;
  let renderTask = null;
  let currentFile = null;

  if (!window.pdfjsLib) {
    showError("Le lecteur PDF n’a pas pu être chargé. Vérifiez votre connexion internet puis rechargez la page.");
    return;
  }
  window.pdfjsLib.GlobalWorkerOptions.workerSrc =
    "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js";

  function showError(message) {
    errorMessage.textContent = message;
    errorMessage.hidden = false;
  }

  function validate(file) {
    if (!file) return "Aucun fichier sélectionné.";
    if (file.type !== "application/pdf" && !file.name.toLowerCase().endsWith(".pdf")) return "Choisissez un fichier au format PDF.";
    if (file.size > MAX_SIZE) return "Ce PDF dépasse la limite de 50 Mo.";
    return "";
  }

  async function openFile(file) {
    const error = validate(file);
    if (error) return showError(error);

    errorMessage.hidden = true;
    currentFile = file;
    el("fileName").textContent = file.name;
    el("fileDetails").textContent = formatBytes(file.size);
    el("extractedText").value = "";
    el("textStatus").textContent = "Ouverture du document…";
    emptyState.hidden = true;
    workspace.hidden = false;

    try {
      const bytes = new Uint8Array(await file.arrayBuffer());
      pdfDocument = await window.pdfjsLib.getDocument({ data: bytes }).promise;
      currentPage = 1;
      el("pageCount").textContent = pdfDocument.numPages;
      el("pageNumber").max = pdfDocument.numPages;
      el("pageNumber").value = 1;
      updatePager();
      await renderPage(1);
      extractAllText();
    } catch (err) {
      reset();
      showError(err && err.name === "PasswordException"
        ? "Ce PDF est protégé par un mot de passe."
        : "Impossible de lire ce PDF. Le fichier est peut-être endommagé.");
    }
  }

  async function renderPage(number) {
    if (!pdfDocument) return;
    if (renderTask) {
      try { renderTask.cancel(); } catch (_) {}
    }
    const page = await pdfDocument.getPage(number);
    const baseViewport = page.getViewport({ scale: 1 });
    const available = Math.max(320, el("canvasWrap").clientWidth - 40);
    const scale = Math.min(2, available / baseViewport.width);
    const viewport = page.getViewport({ scale });
    const ratio = window.devicePixelRatio || 1;

    canvas.width = Math.floor(viewport.width * ratio);
    canvas.height = Math.floor(viewport.height * ratio);
    canvas.style.width = Math.floor(viewport.width) + "px";
    canvas.style.height = Math.floor(viewport.height) + "px";

    renderTask = page.render({
      canvasContext: context,
      viewport,
      transform: ratio === 1 ? null : [ratio, 0, 0, ratio, 0, 0]
    });
    try { await renderTask.promise; } catch (err) {
      if (err && err.name !== "RenderingCancelledException") throw err;
    }
    renderTask = null;
  }

  async function goToPage(number) {
    if (!pdfDocument) return;
    currentPage = Math.max(1, Math.min(pdfDocument.numPages, number));
    el("pageNumber").value = currentPage;
    updatePager();
    await renderPage(currentPage);
  }

  function updatePager() {
    el("prevPage").disabled = !pdfDocument || currentPage <= 1;
    el("nextPage").disabled = !pdfDocument || currentPage >= pdfDocument.numPages;
  }

  async function extractAllText() {
    const pages = [];
    try {
      for (let number = 1; number <= pdfDocument.numPages; number++) {
        el("textStatus").textContent = "Extraction de la page " + number + " sur " + pdfDocument.numPages + "…";
        const page = await pdfDocument.getPage(number);
        const content = await page.getTextContent();
        const text = content.items.map((item) => item.str).join(" ").replace(/\s+/g, " ").trim();
        pages.push("— Page " + number + " —\n" + text);
      }
      const result = pages.join("\n\n");
      el("extractedText").value = result;
      const hasText = result.replace(/— Page \d+ —/g, "").trim().length > 0;
      el("textStatus").textContent = hasText
        ? pdfDocument.numPages + " page" + (pdfDocument.numPages > 1 ? "s" : "") + " extraite" + (pdfDocument.numPages > 1 ? "s" : "")
        : "Aucun texte détecté — ce PDF semble être scanné.";
      el("copyText").disabled = !hasText;
      el("downloadText").disabled = !hasText;
    } catch (_) {
      el("textStatus").textContent = "L’extraction du texte a échoué.";
    }
  }

  function reset() {
    pdfDocument = null;
    currentFile = null;
    input.value = "";
    workspace.hidden = true;
    emptyState.hidden = false;
    el("extractedText").value = "";
    el("copyText").disabled = true;
    el("downloadText").disabled = true;
    context.clearRect(0, 0, canvas.width, canvas.height);
  }

  function formatBytes(bytes) {
    if (!bytes) return "0 octet";
    const units = ["octets", "Ko", "Mo", "Go"];
    const index = Math.min(Math.floor(Math.log(bytes) / Math.log(1024)), units.length - 1);
    return (bytes / Math.pow(1024, index)).toFixed(index ? 1 : 0) + " " + units[index];
  }

  input.addEventListener("change", () => openFile(input.files[0]));
  el("changeFile").addEventListener("click", () => input.click());
  el("prevPage").addEventListener("click", () => goToPage(currentPage - 1));
  el("nextPage").addEventListener("click", () => goToPage(currentPage + 1));
  el("pageNumber").addEventListener("change", (event) => goToPage(Number(event.target.value) || 1));
  dropZone.addEventListener("click", (event) => {
    if (event.target.tagName !== "LABEL") input.click();
  });
  dropZone.addEventListener("keydown", (event) => {
    if (event.key === "Enter" || event.key === " ") { event.preventDefault(); input.click(); }
  });
  ["dragenter", "dragover"].forEach((name) => dropZone.addEventListener(name, (event) => {
    event.preventDefault();
    dropZone.classList.add("is-dragging");
  }));
  ["dragleave", "drop"].forEach((name) => dropZone.addEventListener(name, (event) => {
    event.preventDefault();
    dropZone.classList.remove("is-dragging");
  }));
  dropZone.addEventListener("drop", (event) => openFile(event.dataTransfer.files[0]));

  el("copyText").addEventListener("click", async () => {
    await navigator.clipboard.writeText(el("extractedText").value);
    const button = el("copyText");
    button.textContent = "Copié";
    setTimeout(() => { button.textContent = "Copier"; }, 1500);
  });
  el("downloadText").addEventListener("click", () => {
    const blob = new Blob([el("extractedText").value], { type: "text/plain;charset=utf-8" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = (currentFile ? currentFile.name.replace(/\.pdf$/i, "") : "document") + ".txt";
    link.click();
    URL.revokeObjectURL(link.href);
  });

  let resizeTimer;
  window.addEventListener("resize", () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => renderPage(currentPage), 150);
  });
})();
