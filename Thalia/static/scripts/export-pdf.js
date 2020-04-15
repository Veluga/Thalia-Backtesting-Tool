function exportPDF() {
    var doc = new jsPDF();
    var elementHTML = document.documentElement.innerHTML;
    var specialElementHandlers = {
        '#notThis': function (element, renderer) {
            return true;
        }
    };
    console.log(elementHTML);
    doc.fromHTML(elementHTML, 15, 15, {
        'width': 170,
        'elementHandlers': specialElementHandlers
    }, );

    // Save the PDF
    doc.save('sample-document.pdf');
}