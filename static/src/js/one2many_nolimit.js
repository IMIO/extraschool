openerp.extraschool = function(instance, m) 
{
	
	instance.web.form.widgets = instance.web.form.widgets.extend(
			{
				'one2many_nolimit' : 'instance.web.form.One2ManyNolimit',
			});

	/*
	 * if limit is not defined -> limit by default (80)
	 * if limit = 0 -> unlimited
	 * otherwise limit = the limit defined
	 */
	instance.web.form.One2ManyNolimit = instance.web.form.FieldOne2Many.extend(
	{
        load_views: function() {
        	this._super();
        	try {
                var limit = JSON.parse(this.node.attrs.limit);
                limit = {limit: (limit > 0)?limit:this.dataset.size()};
            } catch(e) {
            	var limit = {};
            }
            _.extend(this.views[0].options, limit || {});
        }
        	
	});

	
}