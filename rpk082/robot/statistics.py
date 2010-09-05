#!/usr/bin/env python

import cairo
import math

def del_all(li,cond):
	i = 0
	while i < len(li):
		if cond(li[i]):
			del li[i:i+1]
			continue
		i += 1
	

def max_element(li,cmpr):
	#find max element in list 'li' using 'cmp' function for compare
	if not len(li):
		return 0
	max_el = li[0]
	for el in li:
		if cmpr(max_el,el):
			max_el = el
	return max_el
	
	
def line(ctx,point1,point2):
	#draw line from point1 to point2 using 'ctx' context
	ctx.move_to(point1[0],point1[1])
	ctx.line_to(point2[0],point2[1])
	
	
def show_text_up(ctx,text,x,y):
	#draw vertical text using 'ctx' context
	(max_x, max_y, max_w, max_h, max_dx, max_dy) = ctx.text_extents(text)
	ctx.rotate(- math.pi / 2)
	ctx.move_to(-y - max_w,x + max_h)
	ctx.show_text(text)
	ctx.rotate(math.pi / 2)
	
	
def draw_grid(ctx,number_of_lines,init_point1,init_point2,dx,dy):
	for i in range(0,number_of_lines):
		line(ctx,init_point1,init_point2)
		init_point1[0] += dx
		init_point2[0] += dx
		init_point1[1] += dy
		init_point2[1] += dy
	ctx.stroke()


def chart(values,width,height,number_of_lvalues,filename):
	'''chart(values,width,height,number_of_lvalues,filename)
	
	draw chart and save it in the file using: 'values' list, where each element represents dict {'name': description_of_the_given_value,'value': value}, WARNING! list can be modified during this function, 'width' and 'height' - parameters of the chart, 'number_of_lvalues' - number of values at left side of chart, 'filename' - name of png-file, string '*.png' '''
	
	if number_of_lvalues == 1 or len(values) == 1:
		return ''
	
	#define cairo context and surface
	srf = cairo.ImageSurface(cairo.FORMAT_ARGB32,width,height)
	ctx = cairo.Context(srf)
	
	#set font
	ctx.select_font_face('sans-serif')
	ctx.set_font_size(12)
    
	(font_x, font_y, font_w, font_h, font_dx, font_dy) = ctx.text_extents('e')
	(max_x, max_y, max_w, max_h, max_dx, max_dy) = ctx.text_extents(max_element(values,lambda dict1,dict2: len(dict1['name']) < len(dict2['name']))['name']) #longest name
	max_el = max_element(values,lambda dict1,dict2: dict1['value'] < dict2['value'])['value'] #max value of the vector
	
	border_left = len(str(max_el)) * font_w + font_w * 2
	border_top = 10
	border_right = 10
	
	delta_x = (width - border_right - border_left) / (len(values) - 1.0)
	if delta_x <= 0:
		return ''
	
	#show_text or show_text_up will be used:
	is_up = (max_w > delta_x)
	if not is_up:
		border_bottom = 3 * font_h
		border_right = int(max_w / 1.5)
		delta_x = (width - border_right - border_left) / (len(values) - 1.0)
	else:
		border_bottom = max_w + font_w * 2

	delta_y = (height - border_top - border_bottom) / (number_of_lvalues - 1.0)
	if delta_y <= 0:
		return ''
			
	#drawing horizontal grid lines:
	ctx.set_line_width(1)		
	ctx.set_dash([1,3])
	ctx.set_source_rgb(0.4,0.4,0.4)
	draw_grid(ctx,number_of_lvalues,[border_left,border_top],[width - border_right,border_top],0,delta_y)
	
	#drawing left values:
	ctx.set_source_rgb(0,0,0)
	current = border_top
	for i in range(0,number_of_lvalues - 1):
		text = str(max_el + i * max_el / (1 - number_of_lvalues))
		ctx.move_to(border_left - len(text) * font_w - font_w * 2,current + font_h * 2.0/3)
		ctx.show_text(text)
		current += delta_y
	
	
	bottom = height - border_bottom
	height_of_chart = height - border_top - border_bottom
	
	#drawing charts curve:
	ctx.set_dash([])
	ctx.set_source_rgb(0,1,0)
	ctx.set_line_width(2)
	ctx.move_to(border_left, bottom - (values[0]['value'] * height_of_chart) / max_el)
	current = border_left + delta_x
	for value in values[1:]:
		ctx.line_to(current, bottom - (value['value'] * height_of_chart) / max_el) #charts curve
		current += delta_x
	ctx.stroke()
	
	#if there are to many values in 'values' list, some values will be deleted from this list - vertical grid lines and names for them will be drawn for restricted number of values (meanwhile the charts curve already drawn for all values):
	if is_up and font_h * 2 > delta_x:
		list_len = len(values)
		number_of_entries = (width - border_left - border_top) / (font_h * 2.0) #number of entries which must left
		how_many_to_del = list_len / (list_len - number_of_entries)
		to_del = how_many_to_del
		if not to_del > 0:
			return ''
		while to_del < list_len:
			values[int(to_del)]['value'] = -1
			to_del += how_many_to_del
		del_all(values,lambda x: x['value'] == -1)
		delta_x = (width - border_right - border_left) / (len(values) - 1.0)

	#drawing vertical grid lines:
	ctx.set_dash([1,3])
	ctx.set_line_width(1)
	ctx.set_source_rgb(0.4,0.4,0.4)
	draw_grid(ctx,len(values),[border_left,border_top],[border_left,bottom],delta_x,0)
	
	#drawing bottom names:
	ctx.set_source_rgb(0,0,0)
	current = border_left
	for value in values:
		if is_up:
			show_text_up(ctx,value['name'],int(current - font_h / 1.5), bottom + int(font_w * 1.5))
		else:
			ctx.move_to(current - font_w * len(value['name']) / 2, bottom + font_h * 2)
			ctx.show_text(value['name'])
		current += delta_x
	
	#writing to file:
	srf.write_to_png(filename)
	return filename

