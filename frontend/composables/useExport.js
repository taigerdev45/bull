export const useExport = () => {
  const exportToExcel = async (data, filename = 'export.xlsx') => {
    if (!process.client) return
    if (!data || !data.length) return alert("Aucune donnée à exporter")
    
    try {
      const XLSX = await import('xlsx')
      const worksheet = XLSX.utils.json_to_sheet(data)
      const workbook = XLSX.utils.book_new()
      XLSX.utils.book_append_sheet(workbook, worksheet, 'Données')
      XLSX.writeFile(workbook, filename)
    } catch (error) {
      console.error("Erreur Excel:", error)
      alert("Erreur lors de la génération Excel.")
    }
  }

  const exportToPDF = async (headers, rows, filename = 'export.pdf', orientation = 'p') => {
    if (!process.client) return
    if (!rows || !rows.length) return alert("Aucune donnée à exporter")

    try {
      const { jsPDF } = await import('jspdf')
      const autoTable = (await import('jspdf-autotable')).default

      const doc = new jsPDF({
        orientation: orientation,
        unit: 'mm',
        format: 'a4'
      })

      // Header Monochrome
      doc.setFillColor(0, 0, 0)
      doc.rect(0, 0, doc.internal.pageSize.width, 35, 'F')
      
      doc.setTextColor(255, 255, 255)
      doc.setFontSize(20)
      doc.setFont('helvetica', 'bold')
      doc.text('BULL ASUR - GESTION ACADÉMIQUE', 15, 18)
      
      doc.setFontSize(9)
      doc.setFont('helvetica', 'normal')
      doc.text(`Document : ${filename.toUpperCase()}`, 15, 28)
      doc.text(`Date : ${new Date().toLocaleDateString()}`, doc.internal.pageSize.width - 60, 28)

      // Tableau Monochrome
      doc.autoTable({
        head: [headers],
        body: rows,
        startY: 40,
        theme: 'grid',
        styles: { fontSize: 8, cellPadding: 3 },
        headStyles: { fillColor: [0, 0, 0], textColor: 255, fontStyle: 'bold' },
        alternateRowStyles: { fillColor: [245, 245, 245] }
      })

      doc.save(filename)
    } catch (error) {
      console.error("Erreur PDF:", error)
      alert("Erreur lors de la génération PDF.")
    }
  }

  return { exportToExcel, exportToPDF }
}
