# Seclytics FortiSOAR Connector

This is Seclytics integration with Fortinet's FortiSoar product.  It provides:
    - Get IP, Domain, Host, or File hash from the Seclytics API.
    - Download Seclytics Prediction data from the API (for security orchestration)

### Build
    - The code is built and tested on FortiSOAR v7.0.1-628 from our AWS instance.
    - The FortiSOAR has an U/I editor to allow editing & testing of the code.
    - The connector can be exported by fortiSOAR U/I as .tgz file.

### Connector Log file
    - log on to FortiSOAR server
    - sudo tail -F /var/log/cyops/cyops-integrations/connectors.log
    - Change log level here: sudo vi /opt/cyops-integrations/integrations/configs/config.ini
    - restart with: sudo systemctl restart uwsgi

### Deployment
    - The directory of the project is compressed into tgz file with tar command.
    - The tgz file can be imported by FortiSOAR

### Change log
    - v1.0.1: The initial version.
