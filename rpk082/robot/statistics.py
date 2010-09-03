#!/usr/bin/env python

import cairo
import math


def max_element(li,cmpr):
	if not len(li):
		return 0
	max_el = li[0]
	for el in li:
		if cmpr(max_el,el):
			max_el = el
	return max_el
	
	
def line(ctx,point1,point2):
	ctx.move_to(point1[0],point1[1])
	ctx.line_to(point2[0],point2[1])
	
	
def show_text_up(ctx,text,x,y):
	(max_x, max_y, max_w, max_h, max_dx, max_dy) = ctx.text_extents(text)
	ctx.rotate(- math.pi / 2)
	ctx.move_to(-y - max_w,x + max_h)
	ctx.show_text(text)
	ctx.rotate(math.pi / 2)


def chart(values,width,height,number_of_lvalues,filename):
	if number_of_lvalues == 1 or len(values) == 1:
		return ''
	
	srf = cairo.ImageSurface(cairo.FORMAT_ARGB32,width,height)
	ctx = cairo.Context(srf)
	
	ctx.select_font_face('sans-serif')
	ctx.set_font_size(12)
    
	(font_x, font_y, font_w, font_h, font_dx, font_dy) = ctx.text_extents('e')
		
	border_right = 10
	(max_x, max_y, max_w, max_h, max_dx, max_dy) = ctx.text_extents(max_element(values,lambda dict1,dict2: len(dict1['name']) < len(dict2['name']))['name']) #longest name's length
	
	max_el = max_element(values,lambda dict1,dict2: dict1['value'] < dict2['value'])['value'] #max value of the vector
	
	border_left = len(str(max_el)) * font_w + font_w * 2
	border_top = 10
	is_up = True

	#drawing horizontal grid lines & left values begin
	ctx.set_line_width(1)
	delta_x = (width - border_right - border_left) / (len(values) - 1.0)
	if delta_x <= 0:
		return ''

	is_up = (max_w > delta_x) #string or stringUp will be used
	if not is_up:
		border_bottom = 3 * font_h
		border_right = int(max_w / 1.5)
		delta_x = (width - border_right - border_left) / (len(values) - 1.0)
	else:
		border_bottom = max_w + font_w * 2
	
	current = border_top
	delta_y = (height - border_top - border_bottom) / (number_of_lvalues - 1.0)
	if delta_y <= 0:
		return ''
	bottom = width - border_right
	
	ctx.set_dash([1,3])
	for i in range(0,number_of_lvalues):
		ctx.set_source_rgb(0.4,0.4,0.4)
		line(ctx,(border_left, current),(bottom, current))
		if i == int(number_of_lvalues) - 1:
			break
		text = str(max_el + i * max_el / (1 - number_of_lvalues))
		
		ctx.move_to(border_left - len(text) * font_w - font_w * 2,current + font_h * 2.0/3)
		ctx.set_source_rgb(0,0,0)
		ctx.show_text(text)
		current += delta_y
	ctx.stroke()
	#drawing horizontal grid lines & left values end
	
	
	#ddrawing vertical grid lines, charts curve & bottom names begin
	bottom = height - border_bottom
	height_of_chart = height - border_top - border_bottom
	
	ctx.set_dash([])
	ctx.set_source_rgb(0,1,0)
	ctx.set_line_width(2)
	ctx.move_to(border_left, bottom - (values[0]['value'] * height_of_chart) / max_el)
	current = border_left + delta_x
	for value in values[1:]:
		ctx.line_to(current, bottom - (value['value'] * height_of_chart) / max_el)
		current += delta_x
	ctx.stroke()
	
	
	number_of_entries = 0
	to_print = 0
	if is_up and font_h * 2 > delta_x:
		number_of_entries = (width - border_left - border_top) / (font_h * 2.0)
	i = 0
	
	current = border_left
	ctx.set_dash([1,3])
	ctx.set_line_width(1)
	for value in values:
		ctx.set_source_rgb(0.4,0.4,0.4)
		if number_of_entries:
			if i < to_print:
				if value == values[:-1][0]:
					line(ctx,(width - border_right,border_top),(width - border_right,bottom))
				current += delta_x
				continue
			else:
				to_print += len(values) / number_of_entries
		line(ctx,(int(current), border_top),(int(current), bottom))
		ctx.set_source_rgb(0,0,0)
		if is_up:
			show_text_up(ctx,value['name'],int(current - font_h / 1.5), bottom + int(font_w * 1.5))
		else:
			ctx.move_to(current - font_w * len(value['name']) / 2, bottom + font_h * 2)
			ctx.show_text(value['name'])
	
		current += delta_x
		i += 1
	ctx.stroke()
	#drawing vertical grid lines, charts curve & bottom names end

	srf.write_to_png(filename)
	return filename

