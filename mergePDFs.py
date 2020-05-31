def mergePDFs( filePath, filename, remove_last_page ):

    # remove_last_page is True or False. if True, then will omit the last page of each pdf.
    # This is helpful for pdfs from HBR, which all have a page tacked on at the end

    #Python script to merge multiple PDF files into one PDF
    # https://geektechstuff.com/2018/02/17/python-3-merge-multiple-pdfs-into-one-pdf/

    #Requires the “PyPDF2” and “OS” modules to be imported
    import os, PyPDF2
    print('HERE')

    # return

    # #Ask user where the PDFs are
    # userpdflocation=input('Folder path to PDFs that need merging:')
    userpdflocation = filePath

    # #Sets the scripts working directory to the location of the PDFs
    os.chdir(userpdflocation)

    # #Ask user for the name to save the file as
    # userfilename=input('What should I call the file?')
    userfilename = filename

    # #Get all the PDF filenames
    pdf2merge = []
    filenames = os.listdir('.')

    # Order filenames by file creation time
    # https://stackoverflow.com/questions/168409/how-do-you-get-a-directory-listing-sorted-by-creation-date-in-python/168424#168424
    # https://geektechstuff.com/2018/02/17/python-3-merge-multiple-pdfs-into-one-pdf/

    search_dir = '.'
    # os.chdir('.')
    filenames = filter(os.path.isfile, os.listdir(search_dir))
    filenames = [os.path.join(search_dir, f) for f in filenames] # add path to each file
    filenames.sort(key=lambda x: os.path.getmtime(x))

    for filename in filenames:
        if filename.endswith('.pdf'):
            pdf2merge.append(filename)

    pdfWriter = PyPDF2.PdfFileWriter()

    #loop through all PDFs
    for filename in pdf2merge:
        #rb for read binary
        pdfFileObj = open(filename,'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        #Opening each page of the PDF

        if remove_last_page:
            last = -1
        else:
            last = 0

        for pageNum in range(pdfReader.numPages + last):
            pageObj = pdfReader.getPage(pageNum)
            pdfWriter.addPage(pageObj)
    #save PDF to file, wb for write binary
    pdfOutput = open(userfilename+'.pdf', 'wb')
    #Outputting the PDF
    pdfWriter.write(pdfOutput)
    #Closing the PDF writer
    pdfOutput.close()

    return