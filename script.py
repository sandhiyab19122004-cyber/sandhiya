document.addEventListener('DOMContentLoaded', function() {
    // Tab Switching Functionality
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabPanes = document.querySelectorAll('.tab-pane');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Remove active class from all buttons and panes
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabPanes.forEach(pane => pane.classList.remove('active'));
            
            // Add active class to clicked button
            button.classList.add('active');
            
            // Show corresponding tab pane
            const tabId = button.getAttribute('data-tab');
            document.getElementById(tabId).classList.add('active');
        });
    });
    
    // Vehicle Make and Model Relationship
    const makeSelect = document.getElementById('make');
    const modelSelect = document.getElementById('model');
    
    // Car models by make
    const carModels = {
        toyota: ['Corolla', 'Camry', 'RAV4', 'Prius', 'Highlander'],
        honda: ['Civic', 'Accord', 'CR-V', 'Pilot', 'Fit'],
        ford: ['F-150', 'Escape', 'Explorer', 'Mustang', 'Focus'],
        chevrolet: ['Silverado', 'Equinox', 'Malibu', 'Tahoe', 'Suburban'],
        tesla: ['Model 3', 'Model Y', 'Model S', 'Model X', 'Cybertruck']
    };
    
    // Update models when make changes
    makeSelect.addEventListener('change', function() {
        const selectedMake = this.value;
        
        // Clear and disable model select if no make is selected
        if (!selectedMake) {
            modelSelect.innerHTML = '<option value="" disabled selected>Select model</option>';
            modelSelect.disabled = true;
            return;
        }
        
        // Enable model select
        modelSelect.disabled = false;
        
        // Populate models based on selected make
        let options = '<option value="" disabled selected>Select model</option>';
        carModels[selectedMake].forEach(model => {
            options += <option value="${model.toLowerCase()}">${model}</option>;
        });
        
        modelSelect.innerHTML = options;
    });
    
    // Slider for City/Highway Driving
    const cityDrivingSlider = document.getElementById('city_driving_percent');
    const cityDrivingValue = document.getElementById('city-driving-value');
    const highwayDrivingValue = document.getElementById('highway-driving-value');
    
    cityDrivingSlider.addEventListener('input', function() {
        const cityPercent = this.value;
        const highwayPercent = 100 - cityPercent;
        
        cityDrivingValue.textContent = cityPercent;
        highwayDrivingValue.textContent = highwayPercent;
    });
    
    // Slider for Annual Mileage
    const annualMileageSlider = document.getElementById('annual_miles');
    const annualMileageValue = document.getElementById('annual-mileage-value');
    
    annualMileageSlider.addEventListener('input', function() {
        const mileage = parseInt(this.value);
        annualMileageValue.textContent = mileage.toLocaleString();
    });
    
    // Form Submission
    const vehicleForm = document.getElementById('vehicle-form');
    
    vehicleForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Validate form
        const make = makeSelect.value;
        const model = modelSelect.value;
        
        if (!make || !model) {
            alert('Please select both vehicle make and model.');
            return;
        }
        
        // Collect form data
        const formData = {
            make: makeSelect.value,
            model: modelSelect.value,
            year: document.getElementById('year').value,
            engineSize: document.getElementById('engine_size').value,
            fuelType: document.getElementById('fuel_type').value,
            transmission: document.getElementById('transmission').value,
            condition: document.getElementById('condition').value,
            maintenance: document.getElementById('maintenance').value,
            usage: document.getElementById('usage').value,
            climate: document.getElementById('climate').value,
            cityDriving: document.getElementById('city_driving_percent').value,
            annualMiles: document.getElementById('annual_miles').value
        };
        
        // In a real application, you would send this data to a server
        console.log('Vehicle Analysis Data:', formData);
        
        // Simulate analysis completion
        simulateAnalysis(formData);
    });
    
    // Simulate analysis and show results
    function simulateAnalysis(formData) {
        // Show loading state
        const analyzeButton = vehicleForm.querySelector('button[type="submit"]');
        const originalText = analyzeButton.textContent;
        analyzeButton.textContent = 'Analyzing...';
        analyzeButton.disabled = true;
        
        // Simulate API call delay
        setTimeout(() => {
            // Reset button
            analyzeButton.textContent = originalText;
            analyzeButton.disabled = false;
            
            // Generate mock results
            const results = generateMockResults(formData);
            
            // Update results tab
            updateResultsTab(results);
            
            // Switch to results tab
            document.querySelector('[data-tab="results"]').click();
        }, 1500);
    }
    
    // Generate mock analysis results
    function generateMockResults(formData) {
        // Calculate base emissions based on engine size and fuel type
        let baseEmissions = 0;
        switch (formData.fuelType) {
            case 'gasoline':
                baseEmissions = 8.887 * parseFloat(formData.engineSize);
                break;
            case 'diesel':
                baseEmissions = 10.180 * parseFloat(formData.engineSize);
                break;
            case 'electric':
                baseEmissions = 0;
                break;
            case 'hybrid':
                baseEmissions = 4.890 * parseFloat(formData.engineSize);
                break;
        }
        
        // Adjust for annual mileage
        const annualMiles = parseInt(formData.annualMiles);
        const annualEmissions = baseEmissions * annualMiles / 1000;
        
        // Adjust for city/highway split
        const cityPercent = parseInt(formData.cityDriving) / 100;
        const highwayPercent = 1 - cityPercent;
        const adjustedEmissions = annualEmissions * (cityPercent * 1.3 + highwayPercent * 0.8);
        
        // Calculate efficiency score (0-100)
        let efficiencyScore = 0;
        if (formData.fuelType === 'electric') {
            efficiencyScore = 95;
        } else if (formData.fuelType === 'hybrid') {
            efficiencyScore = 80;
        } else {
            // Base score on engine size and fuel type
            const baseScore = formData.fuelType === 'gasoline' ? 60 : 50;
            efficiencyScore = Math.max(0, baseScore - (parseFloat(formData.engineSize) - 1.5) * 10);
        }
        
        // Adjust for vehicle condition and maintenance
        if (formData.condition === 'excellent') efficiencyScore += 5;
        if (formData.condition === 'poor') efficiencyScore -= 10;
        if (formData.maintenance === 'regular') efficiencyScore += 5;
        if (formData.maintenance === 'minimal') efficiencyScore -= 8;
        
        // Ensure score is within 0-100 range
        efficiencyScore = Math.min(100, Math.max(0, efficiencyScore));
        
        // Generate recommendations
        const recommendations = [];
        
        if (formData.fuelType !== 'electric') {
            recommendations.push('Consider transitioning to an electric or hybrid vehicle for your next purchase.');
        }
        
        if (parseInt(formData.cityDriving) > 70) {
            recommendations.push('Your high city driving percentage increases emissions. Consider carpooling or public transit for city commutes.');
        }
        
        if (formData.maintenance !== 'regular') {
            recommendations.push('Regular vehicle maintenance can improve fuel efficiency by up to 10%. Schedule your next service soon.');
        }
        
        if (parseInt(formData.annualMiles) > 15000) {
            recommendations.push('Your annual mileage is above average. Consider trip combining or alternative transportation for some journeys.');
        }
        
        // Add general recommendations
        recommendations.push('Maintain proper tire pressure to improve fuel efficiency.');
        recommendations.push('Remove excess weight from your vehicle to reduce fuel consumption.');
        
        return {
            emissions: {
                annual: Math.round(adjustedEmissions * 10) / 10,
                monthly: Math.round(adjustedEmissions / 12 * 10) / 10,
                perMile: Math.round(adjustedEmissions / annualMiles * 1000) / 1000
            },
            scores: {
                efficiency: Math.round(efficiencyScore),
                environmental: Math.round(100 - (adjustedEmissions / 100))
            },
            impact: {
                trees: Math.round(adjustedEmissions / 48),
                gasoline: Math.round(annualMiles / (formData.fuelType === 'electric' ? 100 : 25))
            },
            recommendations: recommendations
        };
    }
    
    // Update results tab with analysis data
    function updateResultsTab(results) {
        const resultsPane = document.getElementById('results');
        const cardContent = resultsPane.querySelector('.card-content');
        
        // Create results HTML
        let html = `
            <div class="results-container">
                <div class="results-section">
                    <h3>Carbon Footprint</h3>
                    <div class="metrics-grid">
                        <div class="metric">
                            <div class="metric-value">${results.emissions.annual}</div>
                            <div class="metric-label">Tons CO₂/Year</div>
                        </div>
                        <div class="metric">
                            <div class="metric-value">${results.emissions.monthly}</div>
                            <div class="metric-label">Tons CO₂/Month</div>
                        </div>
                        <div class="metric">
                            <div class="metric-value">${results.emissions.perMile}</div>
                            <div class="metric-label">kg CO₂/Mile</div>
                        </div>
                    </div>
                </div>
                
                <div class="results-section">
                    <h3>Performance Scores</h3>
                    <div class="scores-container">
                        <div class="score-item">
                            <div class="score-label">Efficiency Score</div>
                            <div class="score-bar">
                                <div class="score-fill" style="width: ${results.scores.efficiency}%"></div>
                                <div class="score-value">${results.scores.efficiency}</div>
                            </div>
                        </div>
                        <div class="score-item">
                            <div class="score-label">Environmental Score</div>
                            <div class="score-bar">
                                <div class="score-fill" style="width: ${results.scores.environmental}%"></div>
                                <div class="score-value">${results.scores.environmental}</div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="results-section">
                    <h3>Environmental Impact</h3>
                    <div class="impact-container">
                        <div class="impact-item">
                            <i class="fas fa-tree"></i>
                            <div class="impact-details">
                                <div class="impact-value">${results.impact.trees}</div>
                                <div class="impact-label">Trees needed to offset your annual emissions</div>
                            </div>
                        </div>
                        <div class="impact-item">
                            <i class="fas fa-gas-pump"></i>
                            <div class="impact-details">
                                <div class="impact-value">${results.impact.gasoline}</div>
                                <div class="impact-label">Gallons of gasoline consumed annually</div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="results-section">
                    <h3>Recommendations</h3>
                    <ul class="recommendations-list">
                        ${results.recommendations.map(rec => <li><i class="fas fa-leaf"></i> ${rec}</li>).join('')}
                    </ul>
                </div>
            </div>
        `;
        
        // Update content
        cardContent.innerHTML = html;
        
        // Add CSS for results
        const style = document.createElement('style');
        style.textContent = `
            .results-container {
                padding: 10px 0;
            }
            
            .results-section {
                margin-bottom: 30px;
            }
            
            .results-section h3 {
                color: var(--primary-dark);
                margin-bottom: 15px;
                padding-bottom: 8px;
                border-bottom: 1px solid var(--border-color);
            }
            
            .metrics-grid {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 20px;
            }
            
            .metric {
                
                border-radius: var(--border-radius);
                padding: 15px;
                text-align: center;
            }
            
            .metric-value {
                font-size: 1.8rem;
                font-weight: 700;
                color: var(--primary-dark);
            }
            
            .metric-label {
                font-size: 0.9rem;
                color: var(--text-light);
                margin-top: 5px;
            }
            
            .scores-container {
                display: flex;
                flex-direction: column;
                gap: 20px;
            }
            
            .score-item {
                display: flex;
                flex-direction: column;
                gap: 8px;
            }
            
            .score-label {
                font-weight: 500;
            }
            
            .score-bar {
                height: 24px;
                
                border-radius: 12px;
                position: relative;
                overflow: hidden;
            }
            
            .score-fill {
                height: 100%;
                
                border-radius: 12px;
            }
            
            .score-value {
                position: absolute;
                top: 0;
                right: 10px;
                height: 100%;
                display: flex;
                align-items: center;
                color: white;
                font-weight: 600;
                text-shadow: 0 0 2px rgba(0,0,0,0.5);
            }
            
            .impact-container {
                display: flex;
                flex-direction: column;
                gap: 15px;
            }
            
            .impact-item {
                display: flex;
                align-items: center;
                gap: 15px;
                
                padding: 15px;
                border-radius: var(--border-radius);
            }
            
            .impact-item i {
                font-size: 2rem;
                color: var(--primary-color);
            }
            
            .impact-value {
                font-size: 1.4rem;
                font-weight: 700;
                color: var(--primary-dark);
            }
            
            .recommendations-list {
                list-style: none;
            }
            
            .recommendations-list li {
                padding: 12px 0;
                border-bottom: 1px solid var(--border-color);
                display: flex;
                align-items: flex-start;
                gap: 10px;
            }
            
            .recommendations-list li:last-child {
                border-bottom: none;
            }
            
            .recommendations-list i {
                color: var(--primary-color);
                margin-top: 3px;
            }
            
            @media (max-width: 768px) {
                .metrics-grid {
                    grid-template-columns: 1fr;
                }
            }
        `;
        
        document.head.appendChild(style);
    }
});
