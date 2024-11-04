<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:cml="http://www.xml-cml.org/schema" xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
  xmlns="http://www.w3.org/1999/xhtml" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:gvr="http://validationreport.gazelle.ihe.net/" version="2.0">
<xsl:param name="elapsedTime" />
<xsl:param name="title" />
<xsl:param name="nameFile" />
  <xsl:template match="/">
    <xsl:apply-templates />
  </xsl:template>


  <xsl:template match="gvr:validationReport ">




    <xsl:choose>
      <xsl:when test="@result='PASSED'">
  
	<h2>:white_check_mark:<xsl:value-of select="$nameFile" /> : <xsl:value-of select="@result" /> </h2>       
        
	<p>Validateur : <xsl:value-of select="/gvr:validationReport/gvr:validationOverview/gvr:validationServiceName" />-<xsl:value-of select="/gvr:validationReport/gvr:validationOverview/gvr:validatorID" /></p> 
	<p>Nombre d'erreurs : <xsl:value-of select="//gvr:counters/@numberOfErrors" /></p>
        <p>Nombre de warnings :  <xsl:value-of select="//gvr:counters/@numberOfWarnings" /></p>
        <p>Temps d'execution :  <xsl:value-of select="$elapsedTime"/></p>
        <p>Nombre de règles:  <xsl:value-of select="//gvr:counters/@numberOfConstraints"/></p>

      </xsl:when>
       <xsl:otherwise>

	<h2>:heavy_exclamation_mark: <xsl:value-of select="$nameFile" /> :<xsl:value-of select="@result" /></h2>             
        <p>Validateur : <xsl:value-of select="/gvr:validationReport/gvr:validationOverview/gvr:validationServiceName" />-<xsl:value-of select="/gvr:validationReport/gvr:validationOverview/gvr:validatorID" /></p>
	 <p>Nombre d'erreurs : <xsl:value-of select="//gvr:counters/@numberOfErrors" /></p>
         <p>Nombre de warnings :  <xsl:value-of select="//gvr:counters/@numberOfWarnings" /></p>
         <p>Temps d'execution :  <xsl:value-of select="$elapsedTime"/></p>
         <p>Nombre de règles:  <xsl:value-of select="//gvr:counters/@numberOfConstraints"/></p>


      </xsl:otherwise>
    </xsl:choose>  

<h3>Validation </h3>  

   
		<xsl:apply-templates />
		
		





  </xsl:template>

  <xsl:template match="gvr:subReport">
  


	  <h4>
		   :arrow_forward:<xsl:value-of select="@name" /> :  <xsl:value-of select="@subReportResult" />

            </h4>

    <table class="table table-striped table-hover">
     <xsl:apply-templates />
     </table>

 


  </xsl:template>

    <xsl:template match="gvr:constraint">
	
    <tr>
      <td>	  
		  <xsl:value-of select="@severity" />
	</td>
      <td class=".small"><small>
      <xsl:value-of select="gvr:constraintDescription" />
       <br/>
      <xsl:value-of select="gvr:locationInValidatedObject" />
      </small></td>

    </tr>
	

  

       
    </xsl:template>

  <xsl:template match="*">
    <!-- drop these -->
  </xsl:template>
  
<xsl:template name="break">
  <xsl:param name="text" select="string(.)"/>
  <xsl:choose>
    <xsl:when test="contains($text, '&#xa;')">
      <xsl:value-of select="substring-before($text, '&#xa;')"/>
      <br/>
      <xsl:call-template name="break">
        <xsl:with-param 
          name="text" 
          select="substring-after($text, '&#xa;')"
        />
      </xsl:call-template>
    </xsl:when>
    <xsl:otherwise>
      <xsl:value-of select="$text"/>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>  
  
</xsl:stylesheet>
