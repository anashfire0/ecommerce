<script>
$(document).ready(function(){
	//contact form stuff
	console.log('eCommerce.js is getting ready')
	var contactForm = $('.contact-form')
	var contactFormMethod = contactForm.attr('method')
	var contactFormEndPoint = contactForm.attr('action')
	contactForm.submit(function(event){
		event.preventDefault();
		var contactFormData = contactForm.serialize()
		var thisForm = $(this)
		$.ajax({
			method: contactFormMethod,
			url: contactFormEndPoint,
			data: contactFormData,
			success: function(data){
				thisForm[0].reset()
				$.alert({
					theme: 'material',
					title: data.message,
					content:'We will get back to you',
				})
			},
			error: function(errorData){
				console.log(errorData)
				var jsonData = errorData.responseJSON
				var msg = ''

				$.each(jsonData, function(key, value){
					msg += key + ': ' + value[0].message
				})
				$.alert({
					theme: 'material',
					title: 'Contact error',
					content: msg,
				})
			}
		})
	})


	//auto search stuff
	var searchForm = $('.search-form');
	var searchInput = searchForm.find('[name="q"]') //searcch element having attr 'q'
	var searchBtn = searchForm.find('[type="submit"]')	
	var typingTimer;
	var typingInterval = 500 //in ms

	searchInput.keyup(function(event){
		clearTimeout(typingTimer)
		typingTimer = setTimeout(performSearch, typingInterval)
	})

	function displaySearching(){
		searchBtn.addClass('disabled')
		searchBtn.html('<i class="fa fa-spin fa-spinner"></i> Searching...')
	}

	function performSearch(){
		displaySearching()
		var query = searchInput.val()
		setTimeout(function(){
			window.location.href='/search/?q=' + query
		}, 1000)
		}

	//cart stuff
	var productForm = $('.form-product-ajax');

	productForm.submit(function(event){
		event.preventDefault();
		console.log('prevented');
		var thisForm = $(this);
		var actionEndpoint = thisForm.attr("data-endpoint");
		var httpMethod = thisForm.attr("method");
		var formData = thisForm.serialize();

		$.ajax({
			url: actionEndpoint,
			method: httpMethod,
			data: formData,
			success: function(data){
				var submitSpan = thisForm.find('.submit-span');
				console.log(submitSpan.html());
				if (data.added){
					submitSpan.html('<button type="submit" class="btn btn-secondary">Remove from cart</button>');
				} else {
					submitSpan.html('<button type="submit" class="btn btn-info">Add to cart</button>')
				}

				// updating cart count in the navbar
				var navbarCount = $('.navbar-cart-count')
				navbarCount.html('('+ data.cartCount + ')');

				// updating the cart items total
				currentPath = window.location.href;

				if (currentPath.indexOf('cart') != -1){
					refreshCart()
				}
			},
			error: function(errorData){
				$.alert({
					theme: 'bootstrap',
					title:'Something went wrong',
					content:'Cannot perform the action',
				})
			},
		})
	})

	function refreshCart(){
		var currentUrl = window.location.href
		var productRows = $('.cart-product')
		var cartTable = $('.cart-table')
		var cartBody = cartTable.find('.cart-body')

		var refreshCartUrl = '/cart/api/';
		var refreshCartMethod = 'GET';
		var data = {};

		console.log('refreshing cart'	)
		$.ajax({
			url: refreshCartUrl,
			method: refreshCartMethod,
			data: data,
			success: function(data){
				var hiddenCartItemRemoveForm = $(".cart-item-remove-form")
				console.log('success');
				console.log(data);

				if (data.products.length > 0){
					productRows.html('')
					i = data.products.length

					$.each(data.products, function(index, value){
						var newCartItemRemove = hiddenCartItemRemoveForm.clone();
						newCartItemRemove.css('display', 'block')
						newCartItemRemove.find('.cart-item-product-id').val(value.id);

						console.log(value.id)
						console.log(newCartItemRemove.html())

						cartBody.prepend(
							`<tr>
									<th scope="row">`+ i +`</th>
									<td><a href="`+ value.url +`">` + value.name + `</a></td>
									<td>`+value.price+`</td>
									<td>`+newCartItemRemove.html()+`</td>
							</tr>`)
					i--;
					})

					console.log('data is ', data.total)
					$('.cart-subtotal').html(data.subtotal);
					$('.cart-total').html(data.total);
				} else {
					window.location.href = currentUrl;
				}
			},
			error: function(errorData){
				$.alert({
					theme: 'material',
					title:'Something went wrong',
					content:'Cannot perform the action',
				})
			}
		});
	}
});
</script>
