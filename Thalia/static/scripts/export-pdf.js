function exportPDF() {
    var doc = new jsPDF();
    var elementHTML = document.body.innerHTML;
    var specialElementHandlers = {
        '#notThis': function (element, renderer) {
            return true;
        }
    };
    doc.fromHTML(elementHTML, 15, 15, {
        'width': 170,
        'elementHandlers': specialElementHandlers
    });

    // Save the PDF
    doc.save('sample-document.pdf');
}