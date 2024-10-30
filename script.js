let zipCodeMedia = {};
let graffitiData = []; // To store the entire processed dataset
let areaToZip = {}; // To store the mapping of areas to their associated zip codes
let allZips = new Set(); // To store all unique zip codes from the reference data

// Fetch the reference data for area-to-zipcode mapping
fetch('https://raw.githubusercontent.com/nicholastscott/litterlog/main/ref_ziparea.csv')
    .then(response => response.text())
    .then(data => {
        const rows = data.split('\n');
        const areaDropdown = document.getElementById('area'); // interchangeable with 'area'
        const zipDropdown = document.getElementById('zipcode');

        rows.forEach(row => {
            const columns = row.split(',');
            const area = columns[1]; // interchangeable with Neighborhood [2] when toggling the document.getElementById('infoArea').textContent = randomEntry.Neighborhood
            const zipcode = columns[0];

            // Store all unique zip codes
            allZips.add(zipcode);
            allZips = new Set([...allZips].sort((a, b) => parseInt(a) - parseInt(b)));


            if (!areaToZip[area]) {
                areaToZip[area] = [];
                // Create an option for the area
                const option = document.createElement('option');
                option.value = area;
                option.textContent = area;
                areaDropdown.appendChild(option);
            }
            areaToZip[area].push(zipcode);
        });
    });

    async function fetchLookupTable() {  
        const response = await fetch('https://your-server.com/your-data.csv', {  
          method: 'GET'  
        });  
        return await response.text();  
      }  
      
      map.on('load', () => {  
        // Initial data load
        fetchLookupTable().then((csvData) => {  
          updateMapData(csvData);  
        });
        
        // Set up periodic updates
        setInterval(() => {
          fetchLookupTable().then((csvData) => {  
            updateMapData(csvData);  
          });
        }, 60000); // Update every 60 seconds
      });  
      
      function updateMapData(csvData) {  
        // Parse the CSV and update your map source here
        // For example:
        // map.getSource('your-source-id').setData(parsedData);
      }