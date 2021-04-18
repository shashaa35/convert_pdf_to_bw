# STEP 1
# import libraries
import fitz
import io
import os, fitz
from PIL import Image, ImageEnhance
import pathlib

SHARPNESS_FACTOR = 3
WORK_DIRECTORY = 'work'
UPLOADS = 'uploads'

def print_pixel_mat(im):
	pixels = list(im.getdata())
	width, height = im.size
	pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]
	print(pixels)

def extract_images(file, directory):

	# open the file
	pdf_file = fitz.open(UPLOADS+'/'+file)

	# STEP 3
	# iterate over PDF pages
	for page_index in range(len(pdf_file)):
		
		# get the page itself
		page = pdf_file[page_index]
		image_list = page.getImageList()
		
		# printing number of images found in this page
		if image_list:
			print(f"[+] Found a total of {len(image_list)} images in page {page_index}")
		else:
			print("[!] No images found on page", page_index)
		for image_index, img in enumerate(page.getImageList(), start=1):
			

			# get the XREF of the image
			xref = img[0]
			
			# extract the image bytes
			base_image = pdf_file.extractImage(xref)
			image_bytes = base_image["image"]
			
			# get the image extension
			image_ext = base_image["ext"]
			image = Image.open(io.BytesIO(image_bytes))
			image_ext = 'png'
			image_name = f"{page_index+1}_{image_index}.{image_ext}"
			image.save(open(f"{directory}/original-{image_name}", "wb"))

			img = convert_image(image)
			
			img.save(open(f"{directory}/converted-{image_name}", "wb"), dpi=(600,600))
			# break
		# break

def convert_to_pdf(file, directory):
	doc = fitz.open()  # PDF with the pictures
	imgdir = directory  # where the pics are
	imglist = os.listdir(imgdir)  # list of them
	imglist.sort()
	imgcount = len(imglist)  # pic count

	for i, f in enumerate(imglist):
		if 'converted' in f:
			img = fitz.open(os.path.join(imgdir, f))  # open pic as document
			rect = img[0].rect  # pic dimension
			pdfbytes = img.convert_to_pdf()  # make a PDF stream
			img.close()  # no longer needed
			imgPDF = fitz.open("pdf", pdfbytes)  # open stream as PDF
			print(f"[+] Adding page to pdf")
			page = doc.new_page(width = rect.width,  # new page with ...
							height = rect.height)  # pic dimension
			page.show_pdf_page(rect, imgPDF, 0)  # image fills the page

	doc.save(f"{directory}/{file}")

def convert_image(img):
	# thresh = 150
	# fn = lambda x : 255 if x > thresh else 0
	# img = img.convert('L').point(fn, mode='1')
	# img = img.convert('L')
	enhancer = ImageEnhance.Sharpness(img)
	img1 = enhancer.enhance(SHARPNESS_FACTOR)
	# img1.save('s-1.png')
	img = img1.convert(mode="1", dither=Image.NONE)
	# print_pixel_mat(img)
	print(f"[+] Converting image")
	return img

def convert_pdf(file):
	directory = f"{WORK_DIRECTORY}/{file[:-4]}"
	pathlib.Path(directory).mkdir(parents=True, exist_ok=True) 
	# pathlib.Path(directory).mkdir(parents=True, exist_ok=True) 
	extract_images(file, directory)
	convert_to_pdf(file, directory)


