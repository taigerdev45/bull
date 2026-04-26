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

  const generateBulletin = async (studentData, type = 'semestriel') => {
    if (!process.client) return
    try {
      const { jsPDF } = await import('jspdf')
      const autoTable = (await import('jspdf-autotable')).default
      const doc = new jsPDF()

      // Header Officiel
      doc.setFontSize(8)
      doc.text('RÉPUBLIQUE GABONAISE', 105, 10, { align: 'center' })
      doc.text('Union - Travail - Justice', 105, 14, { align: 'center' })
      doc.setFontSize(7)
      doc.text('MINISTERE DE LA COMMUNICATION ET DE L\'ECONOMIE NUMERIQUE', 105, 20, { align: 'center' })
      
      doc.setFontSize(14)
      doc.setFont('helvetica', 'bold')
      doc.text('BULLETIN DE NOTES', 105, 35, { align: 'center' })
      doc.setFontSize(10)
      doc.text(`Type : ${type.toUpperCase()}`, 105, 42, { align: 'center' })

      // Infos Étudiant
      doc.setFontSize(9)
      doc.setFont('helvetica', 'normal')
      doc.text(`Nom : ${studentData.nom} ${studentData.prenom}`, 20, 55)
      doc.text(`Matricule : ${studentData.matricule || 'N/A'}`, 20, 60)
      doc.text(`Promotion : ${studentData.promotion || '2025-2026'}`, 140, 55)
      doc.text(`Date d'édition : ${new Date().toLocaleDateString()}`, 140, 60)

      // Tableau (Mock data pour l'exemple de structure)
      doc.autoTable({
        startY: 70,
        head: [['Unité d\'Enseignement', 'Matière', 'Note / 20', 'Crédits', 'Obs']],
        body: [
          ['UE1 : Fondamentaux', 'Algorithmique', '14.50', '4', 'V'],
          ['', 'Base de données', '12.00', '3', 'V'],
          ['UE2 : Développement', 'Java Avancé', '16.00', '5', 'V'],
          ['', 'Frontend Web', '11.50', '3', 'V'],
        ],
        theme: 'grid',
        headStyles: { fillColor: [0, 0, 0] }
      })

      const finalY = doc.lastAutoTable.finalY + 10
      doc.setFont('helvetica', 'bold')
      doc.text(`MOYENNE GÉNÉRALE : ${studentData.moyenne || '0.00'} / 20`, 20, finalY)
      doc.text(`DÉCISION DU JURY : ${studentData.decision || 'EN ATTENTE'}`, 20, finalY + 7)

      doc.save(`Bulletin_${studentData.nom}_${type}.pdf`)
    } catch (e) {
      console.error(e)
      alert("Échec de la génération du bulletin")
    }
  }

  return { exportToExcel, exportToPDF, generateBulletin }
}
