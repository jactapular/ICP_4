// Employee.java 
// Created by Foad Motalebi
// Modified by Johannes Herrmann - 26/10/2015, 2/11/2015

// Needed for the windows interface
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

// Imports needed for JDBC
//import java.sql.*;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

// Other libraries
import java.util.Date;
import java.util.*;             // Needed for properties
import java.io.*;               // Needed for file I/O

import java.lang.*;

public class Employee extends JFrame
{
	//Variable for frame window
	static JFrame frame;
	//Variable for panel
	static JPanel panel;
	static JPanel root;
	static JPanel logoPanel;

	//Variables for layout
	GridBagLayout gl;
	GridBagConstraints gbc;

	//Variables for labels
	JLabel labelEmployeeId;
	JLabel labelEmployeeFirstName;
	JLabel labelEmployeeLastName;
	
	//Variables for data entry controls
	JTextField textEmployeeId;
	JTextField textEmployeeFirstName;
	JTextField textEmployeeLastName;

	// Variable for data display
	JTextField textDisplay;
	
	//Variables for buttons
	JButton buttonAccept;
	JButton buttonCancel;

	
    //Variable for icon
	Icon logoImage;

	public static void main(String args[])
	{
		new Employee();
	}	

	public Employee()
	{
		super("Employee Details");

		//Initialize the layout variables and set it in the panel
		JPanel logoPanel=new JPanel();
		panel=new JPanel();
		gl = new GridBagLayout();
		gbc = new GridBagConstraints();
		root = (JPanel)getContentPane();
		root.setLayout(new BorderLayout());
		panel.setLayout(gl);
		root.add(panel,"Center");
		root.add(logoPanel,"North");
		
	
		//Create and add controls

		//Initialize the icon
		Icon logoImage = new ImageIcon("SomeImage.gif");
		// Please note for the practice
		// the students should give the full path name
		
		//Initializing labels
		labelEmployeeId = new JLabel("Employee Id :");
		labelEmployeeFirstName = new JLabel("Employee First Name :");
		labelEmployeeLastName= new JLabel("Employee Last Name");
		
		//Initializing text fields
		textEmployeeId = new JTextField(6);
		textEmployeeFirstName = new JTextField(40);
		textEmployeeLastName= new JTextField(100);
		textDisplay = new JTextField(300);
		
		//Initializing Combo boxes
		
		//Initializing Buttons
		buttonAccept = new JButton("Accept");
		buttonCancel = new JButton("Cancel");
	
		//Adding label for Employee Id in the layout
		gbc.anchor = GridBagConstraints.NORTHWEST;
		gbc.gridx = 1;
		gbc.gridy = 10;
		gl.setConstraints(labelEmployeeId,gbc);
		panel.add(labelEmployeeId);

		//Adding text field for Employee Id in the layout
		gbc.anchor = GridBagConstraints.NORTHWEST;
		gbc.gridx = 20;
		gbc.gridy = 10;
		gbc.weightx = 1;
		gbc.fill = GridBagConstraints.HORIZONTAL;
		gl.setConstraints(textEmployeeId,gbc);
		panel.add(textEmployeeId);

		//Adding label for employee first name in the layout
		gbc.anchor = GridBagConstraints.NORTHWEST;
		gbc.gridx = 1;
		gbc.gridy = 13;
		gbc.weightx = 0;
		gbc.fill = GridBagConstraints.NONE;
		gl.setConstraints(labelEmployeeFirstName,gbc);
		panel.add(labelEmployeeFirstName);

		//Adding text field for employee first name in the layout
		gbc.anchor = GridBagConstraints.NORTHWEST;
		gbc.gridx = 20;
		gbc.gridy = 13;
		gbc.fill = GridBagConstraints.HORIZONTAL;
		gl.setConstraints(textEmployeeFirstName,gbc);
		panel.add(textEmployeeFirstName);

		//Adding label for Employee Last Name 
		gbc.anchor = GridBagConstraints.NORTHWEST;
		gbc.gridx = 1;
		gbc.gridy = 16;
		gbc.fill = GridBagConstraints.NONE;
		gl.setConstraints(labelEmployeeLastName,gbc);
		panel.add(labelEmployeeLastName);

		//Adding text field for Employee Last Name 
		gbc.anchor = GridBagConstraints.NORTHWEST;
		gbc.gridx = 20;
		gbc.gridy = 16;
		gbc.fill = GridBagConstraints.HORIZONTAL;
		gl.setConstraints(textEmployeeLastName,gbc);
		panel.add(textEmployeeLastName);

		//Adding accept button to the layout
		gbc.anchor = GridBagConstraints.NORTHWEST;
		gbc.gridx = 11;
		gbc.gridy = 37;
		gbc.fill = GridBagConstraints.NONE;
		gl.setConstraints(buttonAccept,gbc);
		panel.add(buttonAccept);
		validateAction validateButton = new validateAction();
		buttonAccept.addActionListener(validateButton);

		//Adding cancel button to the layout
		gbc.anchor = GridBagConstraints.NORTHWEST;
		gbc.gridx = 14;
		gbc.gridy = 37;
		gl.setConstraints(buttonCancel,gbc);
		panel.add(buttonCancel);  

		//Adding text field for Display
		gbc.anchor = GridBagConstraints.NORTHWEST;
		gbc.gridx = 1;
		gbc.gridy = 46;
		gbc.gridwidth = 100;
		gbc.gridheight = 500;
		gbc.fill = GridBagConstraints.BOTH;
		gl.setConstraints(textDisplay,gbc);
		panel.add(textDisplay);
		

		setSize(600,800);
		setVisible(true);
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
	}

//Listener interface implementation for the button
class validateAction implements ActionListener
{
	String SEmployeeID;
	String SEmployeeFirstName;
	String SEmployeeLastName;
	
	public void actionPerformed(ActionEvent evt)
	{
		//Extracting source of action
		Object obj = evt.getSource();
		if(obj == buttonAccept)
		{	

			SEmployeeID=textEmployeeId.getText();
			SEmployeeFirstName=textEmployeeFirstName.getText();
			SEmployeeLastName=textEmployeeLastName.getText();

			// Properties file usage taken from https://community.oracle.com/thread/1262566?start=0&tstart=0
			Properties props = new Properties();
			try
			{
			    InputStream in = getClass().getResourceAsStream("/DbService.properties");
			    if (in == null)
			    {
				throw new NullPointerException("Could not find /DbService.properties");
			    }
			    props.load(in);
			}
			catch (IOException e)
			{
			    throw new RuntimeException("Error loading dbservices.properties from classpath.", e);
			}

	
			ResultSet rs = null;
			Statement stmt = null;
			Connection con = null;
			buttonAccept.setText("Trying ...");
			try
			{
				Class.forName("com.mysql.jdbc.Driver");
			}
			catch (Exception e)
			{
			    System.out.println("Error "+e);
			}

			try
			{
				//establish connection with the data source
				con = DriverManager.getConnection("jdbc:mysql://localhost/ds","me","dsunitpassword");

				//Create the statement object
				PreparedStatement stat = con.prepareStatement("INSERT INTO Emp (empno, firstname, midinit, lastname ) VALUES (?, ?, 'X', ? )");

				stat.setString(1,SEmployeeID);
				stat.setString(2,SEmployeeFirstName);
				stat.setString(3,SEmployeeLastName);
				stat.executeUpdate();

				// Give the number of tuples in the table
				// In this case we create an empty statement and use the executeQuery() method of the resultSet to get an answer.
				stmt = con.createStatement();
				rs = stmt.executeQuery("SELECT COUNT(empno) FROM Emp;");
				rs.absolute(1); // Moves the cursor to the first row of rs
				// Get the item in the first column of the current row of rs as a string
				textDisplay.setText( "There are " + rs.getString( 1 ) + " tuples in the table." );

				// Display the new table to system out.
				stmt = con.createStatement();
				rs = stmt.executeQuery("SELECT * FROM Emp;");
				rs.absolute(1); // Moves the cursor to the first row of rs
				while (rs.next())
				{
				    String empno = rs.getString("empno");
				    String firstname = rs.getString("firstname");
				    String lastname= rs.getString("lastname");
				    System.out.println(" " + empno + " " + firstname + " " + lastname);
				}

				
			} 
			// Code for exceptions and finally https://dev.mysql.com/doc/connector-j/en/connector-j-usagenotes-statements.html
			catch (SQLException ex)
			{
			    System.out.println("SQLException: " + ex.getMessage());
			    System.out.println("SQLState: " + ex.getSQLState());
			    System.out.println("VendorError: " + ex.getErrorCode());
			}
			finally	// Release resources
			{
			    if (rs != null)
			    {
				try
				{
				    rs.close();
				}
				catch (SQLException sqlEx) { } // ignore

				rs = null;
			    }

			    if (stmt != null)
			    {
				try
				{
				    stmt.close();
				}
				catch (SQLException sqlEx) { } // ignore

				stmt = null;
			    }
			}
			buttonAccept.setText("Accept");
		}
	}
}
}
