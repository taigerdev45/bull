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

      autoTable(doc, {
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
      
      const pageWidth = doc.internal.pageSize.width
      const pageHeight = doc.internal.pageSize.height

      // ─── LOGO & QR CODE (Sécurité) ───
      try {
        doc.addImage('/icon.png', 'PNG', 10, 8, 18, 18)
      } catch (e) {
        doc.setDrawColor(0); doc.rect(10, 8, 18, 18)
      }

      const validationUrl = `https://bull-asur.ga/verify/${studentData.matricule || 'VALID'}`
      const qrApiUrl = `https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=${encodeURIComponent(validationUrl)}`
      try {
        doc.addImage(qrApiUrl, 'PNG', pageWidth - 35, 8, 25, 25)
      } catch (e) {}

      // ─── TITRE PRINCIPAL ───
      doc.setTextColor(20, 20, 80)
      doc.setFontSize(16)
      doc.setFont('times', 'bold')
      doc.text(`Bulletin de notes du Semestre 5`, pageWidth / 2, 18, { align: 'center' })
      doc.setFontSize(10)
      doc.setFont('times', 'italic')
      doc.text(`Année universitaire : 2025/2026`, pageWidth / 2, 23, { align: 'center' })

      // ─── CLASSE INFO (BANDEAU BLEU) ───
      doc.setFillColor(30, 45, 110)
      doc.rect(15, 30, pageWidth - 30, 8, 'F')
      doc.setTextColor(255, 255, 255)
      doc.setFontSize(9)
      doc.setFont('helvetica', 'bold')
      doc.text('Classe : Licence Professionnelle Réseaux et Télécommunications Option Administration et Sécurité des Réseaux (ASUR)', 17, 35.5)

      // ─── INFOS ÉTUDIANT (TABLEAU) ───
      autoTable(doc, {
        startY: 40,
        margin: { left: 15 },
        tableWidth: pageWidth - 30,
        body: [
          ['Nom(s) et Prénom(s)', studentData.nom + ' ' + studentData.prenom],
          ['Date et lieu de naissance', 'Né(e) le 12/05/2004 à Libreville']
        ],
        theme: 'grid',
        styles: { fontSize: 9, cellPadding: 2, textColor: [0, 0, 0] },
        columnStyles: { 
          0: { cellWidth: 50, fontStyle: 'bold', fillColor: [240, 240, 240] }
        }
      })

      // ─── TABLEAU DES NOTES PRINCIPAL ───
      const gradeBody = []
      // UE 5.1
      gradeBody.push([{ content: 'UE5-1 : ENSEIGNEMENT GENERAL', colSpan: 5, styles: { fillColor: [230, 235, 255], fontStyle: 'bold' } }])
      gradeBody.push(['   Anglais technique', '2', '1.00', '14.50', '12.48'])
      gradeBody.push(['   Management d\'équipe', '1', '1.00', '12.00', '11.20'])
      gradeBody.push(['   Droit de l\'informatique', '2', '2.00', '13.00', '13.27'])
      gradeBody.push([{ content: 'Moyenne UE5-1', colSpan: 3, styles: { halign: 'right', fontStyle: 'bold' } }, { content: '13.16', styles: { fontStyle: 'bold' } }, '12.32'])
      
      // UE 5.2
      gradeBody.push([{ content: 'UE5-2 : SYSTEMES ET RESEAUX', colSpan: 5, styles: { fillColor: [230, 235, 255], fontStyle: 'bold' } }])
      gradeBody.push(['   Connaissance des réseaux LAN', '2', '2.00', '15.00', '12.98'])
      gradeBody.push(['   Administration Serveurs Windows', '3', '3.00', '11.00', '10.50'])
      gradeBody.push(['   Administration Linux', '2', '2.00', '10.50', '11.41'])
      gradeBody.push([{ content: 'Moyenne UE5-2', colSpan: 3, styles: { halign: 'right', fontStyle: 'bold' } }, { content: '12.16', styles: { fontStyle: 'bold' } }, '11.63'])

      // Penalites
      gradeBody.push([{ content: 'Pénalités d\'absences', colSpan: 3, styles: { halign: 'right', fontStyle: 'bold' } }, '0 heure(s)', ''])
      
      // Moyenne Semestre
      gradeBody.push([{ content: 'Moyenne Semestre 5', colSpan: 3, styles: { halign: 'right', fontStyle: 'bold', fillColor: [245, 245, 245] } }, { content: studentData.moyenne || '12.66', styles: { fontStyle: 'bold', fillColor: [245, 245, 245] } }, { content: '11.80', styles: { fillColor: [245, 245, 245] } }])

      autoTable(doc, {
        startY: doc.lastAutoTable.finalY + 2,
        margin: { left: 15 },
        tableWidth: pageWidth - 30,
        head: [['', 'Crédits', 'Coefficients', 'Notes de l\'étudiant', 'Moyenne de classe']],
        body: gradeBody,
        theme: 'grid',
        styles: { fontSize: 8, cellPadding: 2 },
        headStyles: { fillColor: [255, 255, 255], textColor: [0, 0, 0], fontStyle: 'bold', halign: 'center' },
        columnStyles: {
          0: { cellWidth: 'auto' },
          1: { halign: 'center', cellWidth: 20 },
          2: { halign: 'center', cellWidth: 25 },
          3: { halign: 'center', cellWidth: 35, fontStyle: 'bold' },
          4: { halign: 'center', cellWidth: 30 }
        }
      })

      // ─── RANG & MENTION ───
      autoTable(doc, {
        startY: doc.lastAutoTable.finalY + 2,
        margin: { left: 15 },
        tableWidth: pageWidth - 30,
        head: [['Rang de l\'étudiant au Semestre', 'Mention']],
        body: [['Non classé', 'Passable']],
        theme: 'grid',
        styles: { fontSize: 8, halign: 'center' },
        headStyles: { fillColor: [240, 240, 240], textColor: [0, 0, 0] }
      })

      // ─── ETAT DE VALIDATION ───
      doc.setFontSize(9)
      doc.setFont('helvetica', 'bold')
      doc.text('Etat de la Validation des Crédits au Semestre 5', pageWidth / 2, doc.lastAutoTable.finalY + 10, { align: 'center' })
      
      autoTable(doc, {
        startY: doc.lastAutoTable.finalY + 12,
        margin: { left: 15 },
        tableWidth: pageWidth - 30,
        head: [['UE5-1', 'UE5-2', 'Crédits validés au Semestre 5']],
        body: [
          ['12 Crédits / 12', '18 Crédits / 18', '30 Crédits / 30'],
          ['UE Acquise par Compensation', 'UE Acquise par Compensation', 'Semestre Acquis par Compensation']
        ],
        theme: 'grid',
        styles: { fontSize: 8, halign: 'center' },
        headStyles: { fillColor: [255, 255, 255], textColor: [0, 0, 0] }
      })

      // ─── DECISION DU JURY ───
      const finalY = doc.lastAutoTable.finalY + 15
      doc.setDrawColor(30, 45, 110)
      doc.setLineWidth(0.8)
      doc.line(15, finalY, pageWidth - 15, finalY)
      
      doc.setFontSize(10)
      doc.text(`Décision du Jury :   ${studentData.decision || 'Semestre 5 validé'}`, 15, finalY + 8)
      doc.line(15, finalY + 15, pageWidth - 15, finalY + 15)

      // ─── FOOTER ───
      doc.setFontSize(9)
      doc.setFont('times', 'bold')
      doc.text(`Fait à Libreville, le ${new Date().toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' })}`, pageWidth / 2, finalY + 25, { align: 'center' })
      doc.text('Le Directeur des Etudes et de la Pédagogie', pageWidth / 2, finalY + 35, { align: 'center' })

      doc.save(`Bulletin_${studentData.nom}_S5.pdf`)
    } catch (e) {
      console.error(e)
      alert("Erreur de génération du bulletin")
    }
  }

  return { exportToExcel, exportToPDF, generateBulletin }
}
