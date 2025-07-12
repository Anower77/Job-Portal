jQuery(function($) {

	'use strict';
	
	$(".loader").delay(1000).fadeOut("slow");
  $("#overlayer").delay(1000).fadeOut("slow");	

	var siteMenuClone = function() {

		$('.js-clone-nav').each(function() {
			var $this = $(this);
			$this.clone().attr('class', 'site-nav-wrap').appendTo('.site-mobile-menu-body');
		});


		setTimeout(function() {
			
			var counter = 0;
      $('.site-mobile-menu .has-children').each(function(){
        var $this = $(this);
        
        $this.prepend('<span class="arrow-collapse collapsed">');

        $this.find('.arrow-collapse').attr({
          'data-toggle' : 'collapse',
          'data-target' : '#collapseItem' + counter,
        });

        $this.find('> ul').attr({
          'class' : 'collapse',
          'id' : 'collapseItem' + counter,
        });

        counter++;

      });

    }, 1000);

		$('body').on('click', '.arrow-collapse', function(e) {
      var $this = $(this);
      if ( $this.closest('li').find('.collapse').hasClass('show') ) {
        $this.removeClass('active');
      } else {
        $this.addClass('active');
      }
      e.preventDefault();  
      
    });

		$(window).resize(function() {
			var $this = $(this),
				w = $this.width();

			if ( w > 768 ) {
				if ( $('body').hasClass('offcanvas-menu') ) {
					$('body').removeClass('offcanvas-menu');
				}
			}
		})

		$('body').on('click', '.js-menu-toggle', function(e) {
			var $this = $(this);
			e.preventDefault();

			if ( $('body').hasClass('offcanvas-menu') ) {
				$('body').removeClass('offcanvas-menu');
				$this.removeClass('active');
			} else {
				$('body').addClass('offcanvas-menu');
				$this.addClass('active');
			}
		}) 

		// click outisde offcanvas
		$(document).mouseup(function(e) {
	    var container = $(".site-mobile-menu");
	    if (!container.is(e.target) && container.has(e.target).length === 0) {
	      if ( $('body').hasClass('offcanvas-menu') ) {
					$('body').removeClass('offcanvas-menu');
				}
	    }
		});
	}; 
	siteMenuClone();


	var sitePlusMinus = function() {
		$('.js-btn-minus').on('click', function(e){
			e.preventDefault();
			if ( $(this).closest('.input-group').find('.form-control').val() != 0  ) {
				$(this).closest('.input-group').find('.form-control').val(parseInt($(this).closest('.input-group').find('.form-control').val()) - 1);
			} else {
				$(this).closest('.input-group').find('.form-control').val(parseInt(0));
			}
		});
		$('.js-btn-plus').on('click', function(e){
			e.preventDefault();
			$(this).closest('.input-group').find('.form-control').val(parseInt($(this).closest('.input-group').find('.form-control').val()) + 1);
		});
	};
	// sitePlusMinus();

   var siteIstotope = function() {
  	/* activate jquery isotope */
	  var $container = $('#posts').isotope({
	    itemSelector : '.item',
	    isFitWidth: true
	  });

	  $(window).resize(function(){
	    $container.isotope({
	      columnWidth: '.col-sm-3'
	    });
	  });
	  
	  $container.isotope({ filter: '*' });

	    // filter items on button click
	  $('#filters').on( 'click', 'button', function(e) {
	  	e.preventDefault();
	    var filterValue = $(this).attr('data-filter');
	    $container.isotope({ filter: filterValue });
	    $('#filters button').removeClass('active');
	    $(this).addClass('active');
	  });
  }

  siteIstotope();

  var fancyBoxInit = function() {
	  $('.fancybox').on('click', function() {
		  var visibleLinks = $('.fancybox');

		  $.fancybox.open( visibleLinks, {}, visibleLinks.index( this ) );

		  return false;
		});
	}
	fancyBoxInit();


	var stickyFillInit = function() {
		$(window).on('resize orientationchange', function() {
	    recalc();
	  }).resize();

	  function recalc() {
	  	if ( $('.jm-sticky-top').length > 0 ) {
		    var elements = $('.jm-sticky-top');
		    Stickyfill.add(elements);
	    }
	  }
	}
	stickyFillInit();


	// navigation
  var OnePageNavigation = function() {
    var navToggler = $('.site-menu-toggle');
   	$("body").on("click", ".main-menu li a[href^='#'], .smoothscroll[href^='#'], .site-mobile-menu .site-nav-wrap li a", function(e) {
    //   e.preventDefault();

      var hash = this.hash;

      $('html, body').animate({
        'scrollTop': $(hash).offset().top
      }, 600, 'easeInOutCirc', function(){
        window.location.hash = hash;
      });

    });
  };
  OnePageNavigation();

  var counterInit = function() {
		if ( $('.section-counter').length > 0 ) {
			$('.section-counter').waypoint( function( direction ) {

				if( direction === 'down' && !$(this.element).hasClass('ftco-animated') ) {

					var comma_separator_number_step = $.animateNumber.numberStepFactories.separator(',')
					$('.number').each(function(){
						var $this = $(this),
							num = $this.data('number');
						$this.animateNumber(
						  {
						    number: num,
						    numberStep: comma_separator_number_step
						  }, 7000
						);
					});
					
				}

			} , { offset: '95%' } );
		}

	}
	counterInit();

	var selectPickerInit = function() {
		$('.selectpicker').selectpicker();
	}
	selectPickerInit();

	var owlCarouselFunction = function() {
		$('.single-carousel').owlCarousel({
	    loop:true,
	    margin:0,
	    nav:true,
	    autoplay: true,
	    items:1,
	    nav: false,
	    smartSpeed: 1000
		});

	}
	owlCarouselFunction();

	var quillInit = function() {

		var toolbarOptions = [
		  ['bold', 'italic', 'underline', 'strike'],        // toggled buttons
		  ['blockquote', 'code-block'],

		  [{ 'header': 1 }, { 'header': 2 }],               // custom button values
		  [{ 'list': 'ordered'}, { 'list': 'bullet' }],
		  [{ 'script': 'sub'}, { 'script': 'super' }],      // superscript/subscript
		  [{ 'indent': '-1'}, { 'indent': '+1' }],          // outdent/indent
		  [{ 'direction': 'rtl' }],                         // text direction

		  [{ 'size': ['small', false, 'large', 'huge'] }],  // custom dropdown
		  [{ 'header': [1, 2, 3, 4, 5, 6, false] }],

		  [{ 'color': [] }, { 'background': [] }],          // dropdown with defaults from theme
		  [{ 'font': [] }],
		  [{ 'align': [] }],

		  ['clean']                                         // remove formatting button
		];

		if ( $('.editor').length > 0 ) {
			var quill = new Quill('#editor-1', {
			  modules: {
			    toolbar: toolbarOptions,
			  },
			  placeholder: 'Compose an epic...',
			  theme: 'snow'  // or 'bubble'
			});
			var quill = new Quill('#editor-2', {
			  modules: {
			    toolbar: toolbarOptions,
			  },
			  placeholder: 'Compose an epic...',
			  theme: 'snow'  // or 'bubble'
			});
		}

	}
	quillInit();
  

});



$('.appointment_date').datepicker({
	'format': 'yyyy-m-d',
	'autoclose': true
  });

// Custom JavaScript for Job Portal - Modern Enhancements

// ===== GLOBAL VARIABLES =====
const CONFIG = {
    animationDuration: 300,
    debounceDelay: 500,
    apiEndpoints: {
        saveJob: '/api/save-job/',
        applyJob: '/api/apply-job/',
        searchJobs: '/api/search-jobs/'
    }
};

// ===== UTILITY FUNCTIONS =====
const Utils = {
    // Debounce function for search inputs
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    // Smooth scroll to element
    scrollToElement: function(element, offset = 0) {
        const targetPosition = element.offsetTop - offset;
        window.scrollTo({
            top: targetPosition,
            behavior: 'smooth'
        });
    },

    // Show notification
    showNotification: function(message, type = 'info', duration = 3000) {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = `
            top: 20px; 
            right: 20px; 
            z-index: 9999; 
            min-width: 300px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        `;
        notification.innerHTML = `
            <i class="icon-${this.getNotificationIcon(type)} mr-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, duration);
    },

    // Get notification icon based on type
    getNotificationIcon: function(type) {
        const icons = {
            success: 'check-circle',
            error: 'exclamation-triangle',
            warning: 'exclamation-triangle',
            info: 'info-circle'
        };
        return icons[type] || 'info-circle';
    },

    // Format date
    formatDate: function(date) {
        return new Intl.DateTimeFormat('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        }).format(new Date(date));
    },

    // Format currency
    formatCurrency: function(amount) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD',
            minimumFractionDigits: 0
        }).format(amount);
    }
};

// ===== ANIMATION CONTROLLER =====
const AnimationController = {
    // Initialize animations
    init: function() {
        this.observeElements();
        this.addScrollAnimations();
    },

    // Observe elements for intersection
    observeElements: function() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate__animated', 'animate__fadeInUp');
                }
            });
        }, observerOptions);

        // Observe all cards and sections
        document.querySelectorAll('.job-card, .company-card, .testimonial-card, .blog-card, .stat-card').forEach(el => {
            observer.observe(el);
        });
    },

    // Add scroll animations
    addScrollAnimations: function() {
        const elements = document.querySelectorAll('[data-animate]');
        elements.forEach(element => {
            const animation = element.getAttribute('data-animate');
            element.classList.add('animate__animated', animation);
        });
    },

    // Animate counter
    animateCounter: function(element, target, duration = 2000) {
        let start = 0;
        const increment = target / (duration / 16);
        
        const timer = setInterval(() => {
            start += increment;
            if (start >= target) {
                element.textContent = target;
                clearInterval(timer);
            } else {
                element.textContent = Math.floor(start);
            }
        }, 16);
    }
};

// ===== FORM VALIDATION =====
const FormValidator = {
    // Initialize form validation
    init: function() {
        this.setupValidation();
        this.setupPasswordToggle();
    },

    // Setup form validation
    setupValidation: function() {
        const forms = document.querySelectorAll('.needs-validation');
        forms.forEach(form => {
            form.addEventListener('submit', (event) => {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            });
        });
    },

    // Setup password visibility toggle
    setupPasswordToggle: function() {
        const toggleButtons = document.querySelectorAll('[data-toggle="password"]');
        toggleButtons.forEach(button => {
            button.addEventListener('click', function() {
                const input = this.previousElementSibling;
                const icon = this.querySelector('i');
                
                if (input.type === 'password') {
                    input.type = 'text';
                    icon.classList.remove('icon-eye');
                    icon.classList.add('icon-eye-slash');
                } else {
                    input.type = 'password';
                    icon.classList.remove('icon-eye-slash');
                    icon.classList.add('icon-eye');
                }
            });
        });
    },

    // Validate email
    validateEmail: function(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    },

    // Show field error
    showFieldError: function(field, message) {
        field.classList.add('is-invalid');
        const errorDiv = field.parentNode.querySelector('.invalid-feedback');
        if (errorDiv) {
            errorDiv.textContent = message;
        }
    },

    // Clear field error
    clearFieldError: function(field) {
        field.classList.remove('is-invalid');
        const errorDiv = field.parentNode.querySelector('.invalid-feedback');
        if (errorDiv) {
            errorDiv.textContent = '';
        }
    }
};

// ===== JOB SEARCH CONTROLLER =====
const JobSearchController = {
    // Initialize job search
    init: function() {
        this.setupSearchForm();
        this.setupFilters();
        this.setupSorting();
    },

    // Setup search form
    setupSearchForm: function() {
        const searchForm = document.getElementById('jobSearchForm');
        if (searchForm) {
            const searchInput = searchForm.querySelector('input[name="search"]');
            if (searchInput) {
                searchInput.addEventListener('input', Utils.debounce(() => {
                    this.performSearch();
                }, CONFIG.debounceDelay));
            }
        }
    },

    // Setup filters
    setupFilters: function() {
        const filterCheckboxes = document.querySelectorAll('input[type="checkbox"][name^="filter_"]');
        filterCheckboxes.forEach(checkbox => {
            checkbox.addEventListener('change', Utils.debounce(() => {
                this.applyFilters();
            }, CONFIG.debounceDelay));
        });
    },

    // Setup sorting
    setupSorting: function() {
        const sortSelect = document.querySelector('select[onchange*="sortJobs"]');
        if (sortSelect) {
            sortSelect.addEventListener('change', (e) => {
                this.sortJobs(e.target.value);
            });
        }
    },

    // Perform search
    performSearch: function() {
        const form = document.getElementById('jobSearchForm');
        if (form) {
            const formData = new FormData(form);
            const params = new URLSearchParams(formData);
            window.location.href = `${window.location.pathname}?${params.toString()}`;
        }
    },

    // Apply filters
    applyFilters: function() {
        const form = document.getElementById('jobSearchForm');
        if (form) {
            const formData = new FormData(form);
            
            // Add checkbox filters
            const checkboxes = document.querySelectorAll('input[type="checkbox"]:checked');
            checkboxes.forEach(checkbox => {
                formData.append(checkbox.name, checkbox.value);
            });
            
            const params = new URLSearchParams(formData);
            window.location.href = `${window.location.pathname}?${params.toString()}`;
        }
    },

    // Sort jobs
    sortJobs: function(sortBy) {
        const currentUrl = new URL(window.location);
        currentUrl.searchParams.set('sort', sortBy);
        window.location.href = currentUrl.toString();
    },

    // Clear filters
    clearFilters: function() {
        window.location.href = window.location.pathname;
    }
};

// ===== JOB INTERACTIONS =====
const JobInteractions = {
    // Initialize job interactions
    init: function() {
        this.setupSaveJob();
        this.setupApplyJob();
        this.setupJobCards();
    },

    // Setup save job functionality
    setupSaveJob: function() {
        const saveButtons = document.querySelectorAll('[data-action="save-job"]');
        saveButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                const jobId = button.getAttribute('data-job-id');
                this.saveJob(jobId, button);
            });
        });
    },

    // Setup apply job functionality
    setupApplyJob: function() {
        const applyButtons = document.querySelectorAll('[data-action="apply-job"]');
        applyButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                const jobId = button.getAttribute('data-job-id');
                this.applyJob(jobId, button);
            });
        });
    },

    // Setup job card interactions
    setupJobCards: function() {
        const jobCards = document.querySelectorAll('.job-card');
        jobCards.forEach(card => {
            card.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-5px)';
                this.style.transition = 'transform 0.3s ease';
            });
            
            card.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0)';
            });
        });
    },

    // Save job
    saveJob: function(jobId, button) {
        // Simulate API call
        button.innerHTML = '<i class="icon-heart text-danger"></i> Saved';
        button.classList.add('btn-success');
        button.classList.remove('btn-outline-secondary');
        
        Utils.showNotification('Job saved successfully!', 'success');
    },

    // Apply job
    applyJob: function(jobId, button) {
        // Simulate API call
        button.innerHTML = '<span class="loading"></span> Applying...';
        button.disabled = true;
        
        setTimeout(() => {
            button.innerHTML = '<i class="icon-check"></i> Applied';
            button.classList.add('btn-success');
            button.classList.remove('btn-primary');
            Utils.showNotification('Application submitted successfully!', 'success');
        }, 2000);
    }
};

// ===== DASHBOARD CONTROLLER =====
const DashboardController = {
    // Initialize dashboard
    init: function() {
        this.setupTabs();
        this.setupCharts();
        this.setupNotifications();
    },

    // Setup tabs
    setupTabs: function() {
        const tabLinks = document.querySelectorAll('[data-bs-toggle="tab"]');
        tabLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const target = document.querySelector(link.getAttribute('data-bs-target'));
                if (target) {
                    // Hide all tab panes
                    document.querySelectorAll('.tab-pane').forEach(pane => {
                        pane.classList.remove('show', 'active');
                    });
                    
                    // Remove active class from all tab links
                    tabLinks.forEach(l => l.classList.remove('active'));
                    
                    // Show target pane and activate link
                    target.classList.add('show', 'active');
                    link.classList.add('active');
                }
            });
        });
    },

    // Setup charts (placeholder for future chart implementation)
    setupCharts: function() {
        // Chart.js or other chart library can be integrated here
        console.log('Charts setup ready for integration');
    },

    // Setup notifications
    setupNotifications: function() {
        const notificationButtons = document.querySelectorAll('[data-action="notification"]');
        notificationButtons.forEach(button => {
            button.addEventListener('click', () => {
                Utils.showNotification('Notification feature coming soon!', 'info');
            });
        });
    }
};

// ===== THEME CONTROLLER =====
const ThemeController = {
    // Initialize theme
    init: function() {
        this.setupThemeToggle();
        this.loadTheme();
    },

    // Setup theme toggle
    setupThemeToggle: function() {
        const themeToggle = document.querySelector('[data-action="toggle-theme"]');
        if (themeToggle) {
            themeToggle.addEventListener('click', () => {
                this.toggleTheme();
            });
        }
    },

    // Toggle theme
    toggleTheme: function() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        
        Utils.showNotification(`Switched to ${newTheme} theme`, 'info');
    },

    // Load theme from localStorage
    loadTheme: function() {
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme) {
            document.documentElement.setAttribute('data-theme', savedTheme);
        }
    }
};

// ===== ACCESSIBILITY CONTROLLER =====
const AccessibilityController = {
    // Initialize accessibility features
    init: function() {
        this.setupKeyboardNavigation();
        this.setupFocusManagement();
        this.setupScreenReaderSupport();
    },

    // Setup keyboard navigation
    setupKeyboardNavigation: function() {
        document.addEventListener('keydown', (e) => {
            // Escape key to close modals
            if (e.key === 'Escape') {
                const modals = document.querySelectorAll('.modal.show');
                modals.forEach(modal => {
                    const modalInstance = bootstrap.Modal.getInstance(modal);
                    if (modalInstance) {
                        modalInstance.hide();
                    }
                });
            }
        });
    },

    // Setup focus management
    setupFocusManagement: function() {
        const focusableElements = document.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
        
        focusableElements.forEach(element => {
            element.addEventListener('focus', function() {
                this.style.outline = '2px solid var(--primary-color)';
                this.style.outlineOffset = '2px';
            });
            
            element.addEventListener('blur', function() {
                this.style.outline = '';
                this.style.outlineOffset = '';
            });
        });
    },

    // Setup screen reader support
    setupScreenReaderSupport: function() {
        // Add ARIA labels to interactive elements
        const buttons = document.querySelectorAll('button:not([aria-label])');
        buttons.forEach(button => {
            if (button.textContent.trim()) {
                button.setAttribute('aria-label', button.textContent.trim());
            }
        });
    }
};

// ===== PERFORMANCE OPTIMIZER =====
const PerformanceOptimizer = {
    // Initialize performance optimizations
    init: function() {
        this.lazyLoadImages();
        this.optimizeAnimations();
    },

    // Lazy load images
    lazyLoadImages: function() {
        const images = document.querySelectorAll('img[data-src]');
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    observer.unobserve(img);
                }
            });
        });

        images.forEach(img => imageObserver.observe(img));
    },

    // Optimize animations
    optimizeAnimations: function() {
        // Reduce motion for users who prefer it
        if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
            document.documentElement.style.setProperty('--transition', 'none');
        }
    }
};

// ===== INITIALIZATION =====
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all controllers
    AnimationController.init();
    FormValidator.init();
    JobSearchController.init();
    JobInteractions.init();
    DashboardController.init();
    ThemeController.init();
    AccessibilityController.init();
    PerformanceOptimizer.init();

    // Add global event listeners
    setupGlobalEventListeners();
});

// ===== GLOBAL EVENT LISTENERS =====
function setupGlobalEventListeners() {
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                Utils.scrollToElement(target, 80);
            }
        });
    });

    // Auto-hide alerts after 5 seconds
    document.querySelectorAll('.alert').forEach(alert => {
        setTimeout(() => {
            if (alert.parentNode) {
                alert.remove();
            }
        }, 5000);
    });

    // Add loading states to forms
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.innerHTML = '<span class="loading"></span> Processing...';
                submitBtn.disabled = true;
            }
        });
    });
}

// ===== EXPORT FOR GLOBAL USE =====
window.JobPortal = {
    Utils,
    AnimationController,
    FormValidator,
    JobSearchController,
    JobInteractions,
    DashboardController,
    ThemeController,
    AccessibilityController,
    PerformanceOptimizer
};