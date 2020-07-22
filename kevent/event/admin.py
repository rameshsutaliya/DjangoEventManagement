from django.contrib import admin

# Register your models here.
from event.models import Guest,Event,MediaLinks,UploadMedai


class GuestInline(admin.StackedInline):
	model=Guest

class MediaLinksInline(admin.TabularInline):
	model=MediaLinks

class UploadMedaiInline(admin.TabularInline):
	model=UploadMedai

class EventAdmin(admin.ModelAdmin):
	inlines=[GuestInline,MediaLinksInline,UploadMedaiInline,]
	list_display=['pk','title','date_start','date_end','event_cate',]
	list_filter = ('date_start','date_end','event_cate',)
	ordering=['-date_start','title','event_cate',]
	empty_value_display = 'unknown'
	list_display_links=['pk',]
	list_editable=['title',]
	list_per_page=50
	search_fields = ['title','body',]
	view_on_site = False
	save_on_top=True
	get_autocomplete_fields=['title','event_cate',]
#	show_full_result_count=True


#FOR Extra css
#	{
#		'classes': ('wide', 'extrapretty'),
#	}



#if any field that we don't want to show to the superuser than put as exclude field
#	exclude=['zipcode',]

'''
	fieldsets = (
        ('Section 1', {
            'fields': ('medialinks','location')
        }),
        ('Section 2', {
            'fields': ('title','description')
        }),
        ('Section 3', {
            'fields': ('sku','barcode','unit', 'unitCost','quantity','minQuantity')
        }),
    )

'''
class MediaLinksAdmin(admin.ModelAdmin):
	model=MediaLinks
	list_display=['mediaType','hyperlink','eventname',]
	list_filter=['mediaType','eventname',]
	ordering=['-eventname']
	empty_value_display = '-empty-'
	list_per_page=50
	search_fields = ['hyperlink','eventname__title',]

#	show_full_result_count=True

class GuestAdmin(admin.ModelAdmin):
	model=Guest
	list_display=['name','organization','profile','email','eventname',]
	list_filter=('eventname','organization','profile')
	ordering = ['name','eventname',]
	empty_value_display = '-empty-'
	list_per_page=10
	radio_fields={'eventname':admin.VERTICAL}
	search_fields = ['name','organization','eventname__title',]
	get_autocomplete_fields=['name','organization','profile','email',]
#	show_full_result_count=True

#	radio_fields={'eventname':admin.HORIZONTAL}

#it looks so cool
#	radio_fields={'eventname':admin.VERTICAL}

class UploadMedaiAdmin(admin.ModelAdmin):
	model=UploadMedai
	list_display=['eventname','somethingSpecific',]
	list_filter=['eventname',]
	ordering=['eventname',]
	empty_value_display = '-empty-'
	list_per_page=20
	search_fields=['somethingSpecific','eventname__title',]
	get_autocomplete_fields=['somethingSpecific',]
#	show_full_result_count=True consume the processing power



#if you want to disable the deletion from the admin just put the action = None for selected can node be deleted in single click.
#	actions = None

#admin.site.add_action(export_selected_objects,'Export_objeccts')
admin.site.register(Guest,GuestAdmin)
admin.site.register(MediaLinks,MediaLinksAdmin)
admin.site.register(UploadMedai,UploadMedaiAdmin)
admin.site.register(Event,EventAdmin)
