
from domain.table_detection.Functions.borderFunc import extract_table, extractText,span
import lxml.etree as etree
import cv2

# Input : table coordinates [x1,y1,x2,y2]
# Output : XML Structure for ICDAR 19 single table
def border(table, image, work_folder_path):
    image_np = image
    imag = image.copy()
    final = extract_table(image_np, 1, work_folder_path=work_folder_path)
    if final is None:
        return None
    X = []
    Y = []
    for x1,y1,x2,y2,x3,y3,x4,y4 in final:
        if x1 not in X:
            X.append(x1)
        if x3 not in X:
            X.append(x3)
        if y1 not in Y:
            Y.append(y1)
        if y2 not in Y:
            Y.append(y2)

    X.sort()
    Y.sort()

    tableXML = etree.Element("table")
    Tcoords = etree.Element("Coords", points=str(table[0])+","+str(table[1])+" "+str(table[2])+","+str(table[3])+" "+str(table[2])+","+str(table[3])+" "+str(table[2])+","+str(table[1]))
    tableXML.append(Tcoords)
    for box in final:
        if box[0]>table[0]-5 and box[1]>table[1]-5 and box[2]<table[2]+5 and box[3]<table[3]+5:
            cellBox = extractText(imag[box[1]:box[3],box[0]:box[4]])
            if cellBox is None:
                continue
            ## to visualize the detected text areas
            #cv2.rectangle(imag,(cellBox[0]+box[0],cellBox[1]+box[1]),(cellBox[2]+box[0],cellBox[3]+box[1]),(255,0,0),2)
            cell = etree.Element("cell")
            end_col,end_row,start_col,start_row = span(box,X,Y)
            cell.set("end-col",str(end_col))
            cell.set("end-row",str(end_row))
            cell.set("start-col",str(start_col))
            cell.set("start-row",str(start_row))

            one = str(cellBox[0]+box[0])+","+str(cellBox[1]+box[1])
            two = str(cellBox[0]+box[0])+","+str(cellBox[3]+box[1])
            three = str(cellBox[2]+box[0])+","+str(cellBox[3]+box[1])
            four = str(cellBox[2]+box[0])+","+str(cellBox[1]+box[1])

            coords = etree.Element("Coords", points=one+" "+two+" "+three+" "+four)

            cell.append(coords)
            tableXML.append(cell)
    ## to visualize the detected text areas
    cv2.imwrite(work_folder_path + "/detected_cells.png", imag)
    return tableXML